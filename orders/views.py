from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import JsonResponse
from .forms import OrderForm, OfferForm
from .models import EquipmentCategory, EquipmentSubCategory, Service, ChatGroup, Offer, Equipment, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from users.models import User
from django.core.paginator import Paginator


class IndexView(TemplateView):
    template_name = 'orders/index.html'
    title = 'GoPytak'


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_object(self, queryset=None):
        """
        Override to use order_id as the primary key and add proper error handling
        """
        if queryset is None:
            queryset = self.get_queryset()

        order_id = self.kwargs.get(self.pk_url_kwarg)

        if not order_id:
            raise Http404("No order ID provided")

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get(order_id=order_id)
        except queryset.model.DoesNotExist:
            raise Http404(f"No order found with ID {order_id}")

        return obj

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template
        """
        context = super().get_context_data(**kwargs)
        order = self.object

        # Get chat groups related to this order
        chats = ChatGroup.objects.filter(order=order)

        # Enhance chat objects with additional information
        chat_list = []
        for chat in chats:
            # Get the latest offer for each chat
            last_offer = Offer.objects.filter(group=chat).order_by('-created_at').first()

            if last_offer:
                # Get the executor (proposer of the offer)
                executor = last_offer.proposer

                chat_data = {
                    'id': chat.id,
                    'executor': executor,
                    'last_offer': last_offer,
                }

                chat_list.append(chat_data)

        context['chats'] = chat_list

        # If an executor is assigned, get their details
        if order.executor_id:
            try:
                context['executor'] = User.objects.get(id=order.executor_id)
            except User.DoesNotExist:
                context['executor'] = None

        # Check if there's an active chat
        active_chat_id = self.request.GET.get('chat_id')
        if active_chat_id:
            context['active_chat_id'] = int(active_chat_id)

        return context


@login_required
def user_orders(request):
    """View for displaying user's orders with filtering and search capabilities."""
    # Get all orders for the current user
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    # Apply filters if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(is_active=status_filter)

    # # Filter by new offers
    # new_offers_filter = request.GET.get('new_offers')
    # if new_offers_filter:
    #     # Get orders with unread offers
    #     orders_with_new_offers = Offer.objects.filter(
    #         order__customer=request.user,
    #         is_read=False
    #     ).values_list('order_id', flat=True).distinct()
    #     orders = orders.filter(order_id__in=orders_with_new_offers)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(title__icontains=search_query)

    # Annotate with new offers count
    # for order in orders:
    #     chat = ChatGroup.objects.filter(order=order).order_by('-created_at').first()
    #     order.new_offers_count = Offer.objects.filter(
    #         order=order,
    #         # is_read=False
    #     ).count()

    # Pagination
    paginator = Paginator(orders, 10)  # 10 orders per page
    page_number = request.GET.get('page', 1)
    orders_page = paginator.get_page(page_number)

    # Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'orders/partials/order_list_p.html', {'orders': orders_page})

    return render(request, 'orders/order-list.html', {'orders': orders_page})



class GetSubcategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_name = request.GET.get('category')
        subcategories = EquipmentSubCategory.objects.filter(category__name=category_name).values_list('name', flat=True)
        return JsonResponse({'subcategories': list(subcategories)})

class GetServicesView(View):
    def get(self, request, *args, **kwargs):
        subcategory_name = request.GET.get('subcategory')
        services = Service.objects.filter(subcategory__name=subcategory_name).values_list('name', flat=True)
        return JsonResponse({'services': list(services)})


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order.html"
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')
    title = "Разместить Заказ"


    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        categories = EquipmentCategory.objects.all()
        subcategories = {}
        services = {}

        for category in categories:
            sb = EquipmentSubCategory.objects.filter(category=category).values_list("name", flat=True)
            subcategories[category.name] = list(sb)  # Ensure it's a JSON-compatible list

            for subcategory_name in sb:
                services[subcategory_name] = list(
                    Service.objects.filter(subcategory__name=subcategory_name).values_list("name", flat=True)
                )

        context['subcategories'] = subcategories  # JSON-serializable dict
        context['categories'] = categories
        context['services'] = services  # JSON-serializable dict
        return context

    def form_valid(self, form):
        form.instance.customer = self.request.user
        s = self.request.POST.get('service')
        sb = self.request.POST.get('subcategory')
        service = Service.objects.get(name=self.request.POST.get('service'))
        subcategory = EquipmentSubCategory.objects.get(name=self.request.POST.get('subcategory'))
        form.instance.subcategory = subcategory
        form.instance.service = service

        response =  super(OrderCreateView, self).form_valid(form)

        create_chat(subcategory, self.object, self.request.user)

        return response


def create_chat(subcategory, order, user):
    equipments = Equipment.objects.filter(subcategory=subcategory)
    for equipment in equipments:
        new_chat = ChatGroup.objects.create(order=order)
        new_chat.members.add(user, equipment.user)
        new_chat.save()
        new_offer = Offer.objects.create(group=new_chat, proposer=user, price=order.price, description=order.description)
        new_offer.save()

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom_name)
    form = OfferForm()
    offers = chat_group.chat_offers.all()
    order = chat_group.order
    last_offer = chat_group.chat_offers.order_by('-created').first()

    if request.user not in chat_group.members.all():
        raise Http404()

    if offers and offers[0].proposer != request.user:
        button = True
    else:
        button = False

    if request.htmx:
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.proposer = request.user

            offer.group = chat_group
            offer.save()
            context = {
                'offer':offer,
                'user':request.user,
            }
            return render(request, 'orders/partials/chat_message_p.html', context)

    context = {
        'chat_messages':offers,
        'form':form,
        'chatroom_name':chatroom_name,
        'button': button,
        'order':order,
        'offer_id':last_offer.offer_id if last_offer else None,
    }
    return render(request, 'orders/chat.html', context)


@login_required
def accept_offer(request, offer_id):
    if request.htmx:
        offer = get_object_or_404(Offer, pk=offer_id)
        if request.user == offer.proposer:
            raise Http404()

        order = offer.group.order
        order.price = offer.price

        for member in offer.group.members.all():
            if member != order.customer:
                order.executor_id = member.id

        order.save()

        all_groups = ChatGroup.objects.filter(order=order)
        for group in all_groups:
            group.delete()

        return redirect('orders:index')



