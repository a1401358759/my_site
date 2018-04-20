# -*- coding: utf-8 -*-


def form_error(form_info):
    error_str = []
    for k, v in form_info.errors.items():
        if k == "__all__":
            error_str.append(v[0])
        else:
            error_str.append(u"%s:%s" % (form_info.fields[k].label, v[0]))

    return error_str
