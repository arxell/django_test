from django.contrib import admin

from . import models


class DealAdminInline(admin.StackedInline):
    extra = 0
    model = models.Deal

    fields = ['amount', 'result_amount']
    readonly_fields = ['amount', 'result_amount']


class TransactionAdminInline(admin.StackedInline):
    extra = 0
    model = models.Transaction

    fields = ['amount', 'type']
    readonly_fields = ['amount', 'type']


class TraderAdmin(admin.ModelAdmin):

    inlines = [
        DealAdminInline,
        TransactionAdminInline,
    ]

    class Meta:
        model = models.Trader


class DealAdmin(admin.ModelAdmin):

    list_display = ['trader', 'amount', 'result_amount', 'created_at']

    class Meta:
        model = models.Deal


class TransactionAdmin(admin.ModelAdmin):

    list_display = ['trader', 'amount', 'type', 'created_at']

    class Meta:
        model = models.Transaction


admin.site.register(models.Trader, TraderAdmin)
admin.site.register(models.Deal, DealAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
