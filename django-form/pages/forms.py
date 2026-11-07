from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    name = forms.CharField(label='Full Name', max_length=100)
    university_id = forms.IntegerField(label='University ID')
    national_id = forms.IntegerField(label='ID Number')
    mobile = forms.CharField(label='Mobile Number')
    address = forms.CharField(label='Address')
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )
    image = forms.ImageField(label='Image')

    class Meta:
        model = Student
        fields = ['name', 'university_id', 'national_id', 'mobile', 'address', 'date_of_birth', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['accept'] = '.jpg,.jpeg,.png'

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        for ch in name:
            if not (ch.isalpha() or ch == ' '):
                raise forms.ValidationError('name must contain letters only, no numbers or symbols')
        return name

    def clean_university_id(self):
        uid = self.cleaned_data['university_id']
        text = str(uid)
        if len(text) != 9:
            raise forms.ValidationError('university id must be exactly 9 digits')
        if text[0] not in '12':
            raise forms.ValidationError('university id must start with 1 or 2')
        if Student.objects.filter(university_id=uid).exists():
            raise forms.ValidationError('this university id is already registered')
        return uid

    def clean_national_id(self):
        nid = self.cleaned_data['national_id']
        text = str(nid)
        if len(text) != 9:
            raise forms.ValidationError('id number must be exactly 9 digits')
        if text[0] not in '984':
            raise forms.ValidationError('id number must start with 9, 8 or 4')
        return nid

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile'].strip()
        if not mobile.isdigit():
            raise forms.ValidationError('mobile number must contain digits only')
        if len(mobile) != 10:
            raise forms.ValidationError('mobile number must be exactly 10 digits')
        if not (mobile.startswith('059') or mobile.startswith('056')):
            raise forms.ValidationError('mobile number must start with 059 or 056')
        return mobile

    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        if len(address) > 150:
            raise forms.ValidationError('address must not exceed 150 characters')
        return address

    def clean_image(self):
        image = self.cleaned_data['image']
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError('image must be jpg or png only')
        return image
