from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # 編集対象にするフィールドを指定します
        fields = ['title', 'due_at', 'completed']
        
        # HTMLでの表示スタイル（classやプレースホルダー）を設定します
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Input title'
            }),
            'due_at': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    # 期限（Due at）が過去の日時になっていないかチェックするバリデーション
    def clean_due_at(self):
        due_at = self.cleaned_data.get('due_at')
        from django.utils import timezone
        
        # 期限が入力されていて、かつ現在時刻より前の場合はエラーを出す
        if due_at and due_at < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past!")
        return due_at