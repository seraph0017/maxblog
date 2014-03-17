#!/usr/bin/env python
#encoding:utf-8
"""
accounts.forms
~~~~~~~~~~~~~~~~~~~~
表单验证文件，注册，登陆验证
"""
from django import forms

class RegisterForm(forms.Form):
    """.. py:class::RegisterForm
    用户注册表单模块
    """
    email = forms.EmailField(label='邮箱',required=True,help_text='请填写您的email')
    username = forms.CharField(label='用户名',required=True,help_text='请填写您的用户名'\
        max_length=20,min_length=1)
    password = forms.CharField(label='密码',required=True,help_text='请填写您的密码'\
        max_length=20,min_length=6,widget=forms.PasswordInput())