# -*- coding: utf-8 -*-
import datetime
from django import forms
from crops_and_markets_app.models import *

# ######## #
# Crops
class CompanyCropFrom(forms.Form): # todo, add required false to required fields
	company_member = forms.BooleanField(required=False)
	excisting_company = forms.ModelChoiceField(required=False, queryset=CompanyCrop.objects.all(), empty_label="Compañía", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	name = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))

	class Meta:
		model = CompanyCrop

	def clean(self):
		checkbox = self.cleaned_data.get('company_member')
		print "CHECK BOX!"
		print checkbox
		if not checkbox:
			return self.cleaned_data
		if self.cleaned_data.get('excisting_company') is not None or self.cleaned_data.get('name') != "":
			return self.cleaned_data
		raise forms.ValidationError('Error validating CompanyCropFrom')


class CropForm(forms.Form):
	region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Región", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	#province =forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="Provincia", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	#commune = todo	... 
	address = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	latitude = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"type": "number", "class": "form-control input-sm"}))
	longitude = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"type": "number", "class": "form-control input-sm"}))

	has = forms.IntegerField(required=False, min_value=0, max_value=32767, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))

	# information about crop core characteristics
	water = forms.BooleanField(required=False)
	soil = forms.BooleanField(required=False)
	topography = forms.BooleanField(required=False)
	temperatures = forms.BooleanField(required=False)

	water_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	soil_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	topography_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	temperatures_cmnt = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))

	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	class Meta:
		model = Crop


class CropOwnerForm(forms.Form):
	# excisting owner
	old_owner = forms.ModelChoiceField(required=False, queryset=CropOwner.objects.all(), empty_label="Propietario registrado", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	# new owner
	first_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	last_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	contact_number_1 = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	contact_number_2 = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
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


# ######## #
# Markets
class ClientForm(forms.Form):
	type_of_client = forms.ModelChoiceField(queryset=TypeOfClient.objects.all(), empty_label="Tipo de cliente", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	contact_number_1 = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	contact_number_2 = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control input-sm"}))
	position = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) # attrs={'placeholder': u'Observaciones'}

	class Meta:
		model = Client
		# exclude = ('campo_a', 'campo_b', 'campo_c')


#class ComercialInformationForm(forms.Form):
#	#volume = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
#	#varieties = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
#	#price (...)

#	class Meta:
#		model = ComercialInformation


class CompanyMarketForm(forms.Form):
	excisting_company = forms.ModelChoiceField(queryset=CompanyMarket.objects.all(), empty_label="Compañía", required=False, widget=forms.Select(attrs={'class':'form-control input-sm'}))
	# new company
	name = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	rut = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))

	class Meta:
		model = CompanyMarket


class GeoMarkerForm(forms.Form):
	region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Región", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	#province = todo
	#commune = todo
	address = forms.CharField(required=False, max_length=256, widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
	latitude = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"type": "number", "class": "form-control input-sm"}))
	longitude = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"type": "number", "class": "form-control input-sm"}))

	class Meta:
		model = GeoMarker


class SaleForm(forms.Form):
	day = forms.DateField(initial=datetime.date.today)
	price = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	variety = forms.ModelChoiceField(queryset=PotatoVariety.objects.all(), empty_label="Variedad", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	volume = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) #to add a placeholder, place this into Textarea() > attrs={'placeholder': u'Observaciones'}

	class Meta: 
		model = Sale


class ReserveForm(forms.Form):
	day = forms.DateField(initial=datetime.date.today)
	price = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	variety = forms.ModelChoiceField(queryset=PotatoVariety.objects.all(), empty_label="Variedad", widget=forms.Select(attrs={'class':'form-control input-sm'}))
	volume = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number', 'class':'form-control input-sm'}))
	observations = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control input-sm"})) #to add a placeholder, place this into Textarea() > attrs={'placeholder': u'Observaciones'}

	class Meta:
		model = Reserve