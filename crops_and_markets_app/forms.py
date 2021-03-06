# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.forms.formsets import formset_factory
from crops_and_markets_app.models import *

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker', 'placeholder': u'mm/dd/aaaa'})

# ######## #
# Crops
class CompanyCropFrom(forms.Form):
	company_member = forms.BooleanField(required=False)
	excisting_company = forms.ModelChoiceField(required=False, queryset=CompanyCrop.objects.all(), empty_label="Seleccione compañía", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	comp_name = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	comp_rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm rut"}))

	class Meta:
		model = CompanyCrop

	def clean(self):
		checkbox = self.cleaned_data.get('company_member')
		if not checkbox:
			return self.cleaned_data
		if self.cleaned_data.get('excisting_company') is not None or self.cleaned_data.get('name') != "":
			return self.cleaned_data
		raise forms.ValidationError('Error validating CompanyCropFrom')


class CropForm(forms.Form):
	name = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccione región", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	address = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))

 	latitude = forms.FloatField(required=False, widget=forms.NumberInput(attrs={"type": "number", "class": "form-control input-sm"}))
 	longitude = forms.FloatField(required=False, widget=forms.NumberInput(attrs={"type": "number", "class": "form-control input-sm"}))
 
	has = forms.FloatField(required=False, min_value=0, max_value=32767, widget=forms.NumberInput(attrs={'type': 'number', 'class':'form-control input-sm'}))

	# information about crop core characteristics
	water = forms.BooleanField(required=False)
	water_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	soil = forms.BooleanField(required=False)
	soil_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	topography = forms.BooleanField(required=False)
	topography_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	temperatures = forms.BooleanField(required=False)
	temperatures_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	access = forms.BooleanField(required=False)
	access_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	class Meta:
		model = Crop


class CropOwnerForm(forms.Form):
	# excisting owner
	old_owner = forms.ModelChoiceField(required=False, queryset=CropOwner.objects.all(), empty_label="Propietario registrado", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	# new owner
	first_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	last_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm rut"}))
	contact_number_1 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	contact_number_2 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control input-sm"}))
	position = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	#observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	class Meta: 
		model = CropOwner

	# def clean_old_owner(self):
	# 	print "clean old owner"
	# 	return self.clean()

	# def clean_first_name(self):
	# 	print "clean first name"
	# 	return self.clean()

	# def clean_last_name(self):
	# 	print "clean last name"
	# 	return self.clean()

	def clean(self):
		old_owner = self.cleaned_data.get('old_owner')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		if old_owner is not None or (first_name != "" and last_name != ""):
			return self.cleaned_data
		raise forms.ValidationError('Error validating CropOwnerForm')


class PlantationForm(forms.Form):
	date = forms.DateField(widget=DateInput())
	crop = forms.ModelChoiceField(queryset=Crop.objects.all(), empty_label="Seleccione Predio", widget=forms.Select(attrs={'class':'form-control input-sm'})) 
	paddock = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	variety = forms.ModelChoiceField(required=True, queryset=PotatoVariety.objects.all(), empty_label="Variedad", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	source_lot = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	kg_seeds = forms.FloatField(widget=forms.NumberInput(attrs={'type': 'number', 'class':'form-control input-sm'}))  
	kg_fert = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	n_mini = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	has = forms.FloatField(min_value=0, max_value=32767, widget=forms.NumberInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	control_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	obs = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"}))

	class Meta: 
		model = Plantation

# ######## #
# Markets
class ClientForm(forms.Form):
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm rut"}))
	contact_number_1 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	contact_number_2 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control input-sm"}))
	position = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	# REFACTOR
	# add geo_info/geo_marker_form here.

	class Meta:
		model = Client
		# exclude = ('campo_a', 'campo_b', 'campo_c')


class ClientTypeForm(forms.Form):
	type_of_client = forms.ModelChoiceField(queryset=TypeOfClient.objects.all(), empty_label="Tipo de cliente", widget=forms.Select(attrs={'class':'form-control input-sm'}))


class CompanyMarketForm(forms.Form):
	excisting_company = forms.ModelChoiceField(queryset=CompanyMarket.objects.all(), empty_label="Seleccione compañía", required=False, widget=forms.Select(attrs={'class':'form-control input-sm'}))
	# new company
	name = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm rut"}))

	class Meta:
		model = CompanyMarket


class GeoMarkerForm(forms.Form):
	region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccione región", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	address = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))

	class Meta:
		model = GeoMarker


class SaleDetailForm(forms.Form):
	price = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	variety = forms.ModelChoiceField(required=True, queryset=PotatoVariety.objects.all(), empty_label="Variedad", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	volume = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	certification = forms.ModelChoiceField(required=True, queryset=Certification.objects.all(), empty_label="Tipo de certificación", widget=forms.Select(attrs={'class':'form-control input-sm'}))

	class Meta:
		model = SaleDetail

SaleDetailFormSet = formset_factory(SaleDetailForm, min_num=1, extra=0, validate_min=True)


class TransactionForm(forms.Form):
	type_of_transaction = forms.ModelChoiceField(queryset=TypeOfTransaction.objects.all(), empty_label="Eliga tipo de transacción", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	date = forms.DateField(widget=DateInput())
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"}))

	class Meta: 
		model = Sale


# ######## #
# Related contacts
class ContactForm(forms.Form):
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm rut"}))
	contact_number_1 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	contact_number_2 = forms.RegexField(required=False, regex=r'^\+?\d{8,11}$', 
		error_message = ("Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed."),
		widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control input-sm"}))
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	related_area = forms.ModelChoiceField(required=False, queryset=RelatedArea.objects.all(), empty_label="Seleccione área", widget=forms.Select(attrs={'class':'form-control input-sm'}))

	class Meta:
		mdoel = Related

