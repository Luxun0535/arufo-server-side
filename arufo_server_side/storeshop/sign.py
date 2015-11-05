#encoding:utf-8
import types
from arufo_server_side import settings
from storeshop.hashcompact import md5_constructor as md5

def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s,str):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, str):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def params_filter(params):
    ks =  sorted(params.keys(),key=lambda d:d[0])
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr

def build_mysign(tn, subject, body , total_fee):
    params = {}
    params['service'] = settings.ALIPAY_SERVER
    params['payment_type'] = settings.ALIPAY_PAYMRMT_TYPE
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_SELLER_ID
    params['it_b_pay'] = settings.ALIPAY_SELLER_IT_B_PAY
    params['notify_url'] = settings.ALIPAY_NOTIFY_URL
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET
    params['out_trade_no'] = tn
    params['subject'] = subject
    params['body'] = body
    params['total_fee'] = total_fee
    params,prestr = params_filter(params)
    #sign= md5(prestr + settings.ALIPAY_KEY).hexdigest()
    sign=build_sign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    return sign

def build_sign(prestr, key, sign_type = 'MD5'):
    if sign_type == 'MD5':
        prestr=prestr.encode(settings.ALIPAY_INPUT_CHARSET)
        key=key.encode(settings.ALIPAY_INPUT_CHARSET)
        return md5(prestr + key).hexdigest()
    return ''
