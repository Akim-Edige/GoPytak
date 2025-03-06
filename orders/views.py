from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import JsonResponse
from .forms import OrderForm, OfferForm
from .models import EquipmentCategory, EquipmentSubCategory, Service, ChatGroup, Offer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


class IndexView(TemplateView):
    template_name = 'orders/index.html'
    title = 'GoPytak'


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
    template_name = "orders/order.html"
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
        return super(OrderCreateView, self).form_valid(form)


@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom_name)
    form = OfferForm()
    offers = chat_group.chat_offers.all()

    if offers[0].proposer != request.user:
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
    }
    return render(request, 'orders/chat.html', context)