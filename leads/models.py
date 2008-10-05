# coding: utf-8
from django.db import models
from django.contrib import admin
from datetime import datetime

# Create your models here.

class ClientCompany(models.Model):
    """Client company"""
    name=models.CharField(max_length=200)
    
    def __unicode__(self): return self.name

class ClientOrganisation(models.Model):
    """A department in client organization"""
    name=models.CharField(max_length=200)
    company=models.ForeignKey(ClientCompany)

    def __unicode__(self): return u"%s : %s " % (self.company, self.name)

class ClientContact(models.Model):
    """A contact in client organization"""
    name=models.CharField("Nom", max_length=200)
    function=models.CharField("Fonction", max_length=200, blank=True)
    email=models.EmailField(blank=True)
    phone=models.CharField("Téléphone", max_length=30, blank=True)
    
    def __unicode__(self): return self.name

class Client(models.Model):
    """A client organization"""
    organisation=models.ForeignKey(ClientOrganisation)
    # Move contact to lead instead of Client ?
    contact=models.ForeignKey(ClientContact)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.organisation, self.contact)

class Consultant(models.Model):
    """A New'Arch consultant"""
    name=models.CharField(max_length=50)
    trigramme=models.CharField(max_length=4)
    #manager=models.ForeignKey(Consultant)

    def __unicode__(self): return self.name

class Lead(models.Model):
    """A commercial lead"""
    STATES = (
                  ('QUALIF', u'En cours de qualification'),
                  ('WRITE_OFFER', u'Proposition à émettre'),
                  ('OFFER_SENT', u'Proposition émise'),
                  ('NEGOCATION', u'Négociation en cours'),
                  ('WIN', u'Affaire gagnée'),
                  ('LOST', u'Affaire perdue'),
                  ('FORGIVEN', u'Affaire abandonnée'),
                  )
    name=models.CharField("Nom", max_length=200)
    description=models.TextField()
    sales=models.IntegerField("CA (k€)", blank=True, null=True)
    staffing=models.ManyToManyField(Consultant, blank=True)
    responsible=models.ForeignKey(Consultant, related_name="%(class)s_responsible", verbose_name="Responsable", blank=True, null=True)
    start_date=models.DateField("Démarrage", blank=True, null=True)
    due_date=models.DateField("Échéance", blank=True, null=True)
    state=models.CharField("État", max_length=30, choices=STATES)
    client=models.ForeignKey(Client)

    creation_date=models.DateTimeField("Création", default=datetime.now())
    update_date=models.DateTimeField("Mise à jour", default=datetime.now())

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.client)

class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "description", "responsible", "sales", "creation_date", "due_date", "update_date")
    fieldsets = [
        (None,    {"fields": ["name", "description", "client"]}),
        ('État et suivi',     {'fields': ['responsible', 'start_date', 'state', 'due_date']}),
        ('Staffing',     {'fields': ["staffing", "sales"]}),
        ]
    ordering = ("creation_date",)
    filter_horizontal=["staffing"]
    list_filter = ["state",]
    date_hierarchy = "creation_date"
    search_fields = ["name", "responsible__name", "description"]

class ClientContactAdmin(admin.ModelAdmin):
    list_display=("name", "function", "email", "phone")
    odering=("name")
    search_fields=["name", "function"]

admin.site.register(Lead, LeadAdmin)
admin.site.register(Client)
admin.site.register(ClientOrganisation)
admin.site.register(ClientCompany)
admin.site.register(ClientContact, ClientContactAdmin)
admin.site.register(Consultant)
