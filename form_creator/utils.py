from django import forms

from form_creator.forms import SuperForm

def load_json(fields: list[dict], create_formset: bool = False, formset_name = None) -> list[SuperForm | forms.BaseFormSet] | forms.BaseFormSet:
    '''
    returns list of forms/formsets
    json description:
        {
            "name": str, Name of the field,

            "type": Literal["string", "int", "formset"], type of field 
            
            // formset -- набор форм. чтобы пользователь мог сам создавать эти формы, можно воспользоваться инструкцией https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript

            "kwargs": dict, kwargs to pass into field constructor 

            // ^^^ all the magic possibly is here ^^^, to customize forms more we need to learn 
                how to properly dump all the kwargs you need into json and how to load them back    
        }
    '''
    field_name_to_class_map = {
        'string': forms.CharField,
        'int': forms.IntegerField,
    }
    cur_form_fields = {}
    result_list = []
    i=0
    for field in fields:
        if create_formset and isinstance(field, list):
            AssertionError(f'Невозможно распознать {field} как поле для формы в formset-е')
        if field['type'] == 'formset':
            if cur_form_fields:
                result_list.append(SuperForm(prefix = 'form_'+str(i:=i+1), dynamic_fields=cur_form_fields))
            result_list.append(load_json(field['fields'], create_formset=True, formset_name=field['name']))
        else:
            cur_form_fields[field['name']] = field_name_to_class_map[field['type']](**field.get('kwargs', {}))
    if create_formset:
        return forms.formset_factory(SuperForm)(prefix = formset_name, form_kwargs = dict(dynamic_fields=cur_form_fields))
    if cur_form_fields:
        result_list.append(SuperForm(prefix = 'form_'+str(i:=i+1), dynamic_fields=cur_form_fields))
    return result_list
        


def get_forms_example():
    return load_json(
        [
            {'name':'name', 'type':'string'},
            {'name':'surname', 'type':'string'},
            {'name':'age', 'type':'int'},
            {'name': 'Дети', 'type':'formset', 'fields':[
                {'name':'name', 'type':'string'},
                {'name':'surname', 'type':'string'},
                {'name':'age', 'type':'int'},
            ]}
        ]
    )