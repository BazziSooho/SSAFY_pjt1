# savings.models
from django.db import models
from django.conf import settings

# Create your models here.
class SavingProduct(models.Model):
    dcls_month = models.IntegerField(verbose_name='공시제출월')  # 공시제출월
    fin_co_no = models.IntegerField()                   # 금융회사코드
    kor_co_nm = models.CharField(max_length=50, verbose_name='은행이름') 
    fin_prdt_cd = models.TextField(unique=True)         # 금융상품코드
    fin_prdt_nm = models.TextField()                    # 상품이름
    join_way = models.TextField()                       # 가입방법
    mtrt_int = models.TextField(verbose_name='만기후이자율')       # 만기후 이자율
    spcl_cnd = models.TextField(verbose_name='우대사항') # 우대사항
    join_deny = models.IntegerField()                   # {1:제한없음, 2:서민전용, 3:일부제한}
    join_member = models.TextField()                    # 가입대상
    etc_note = models.TextField()                       # 비고(가입한도, 방식 등)
    max_limit = models.IntegerField(null=True)          # 최대한도
    dcls_strt_day = models.IntegerField(verbose_name='공시 시작일')     # 공시 시작일
    dcls_end_day = models.IntegerField(verbose_name='공시 종료일', null=True)    # 공시 종료일
    fin_co_subm_day = models.IntegerField(verbose_name='금융회사 제출일')   # 금융회사 제출일

    class Meta:
        verbose_name = "적금 상품"
        verbose_name_plural = "적금 상품 목록"

    

class ProductInterest(models.Model):
    fin_prdt_cd = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, to_field='fin_prdt_cd')        # 금융상품코드
    dcls_month = models.IntegerField()      # 공시제출월
    fin_co_no = models.IntegerField()       # 금융회사코드
    intr_rate_type = models.CharField(max_length=10, verbose_name='금리 유형')
    intr_rate_type_nm = models.TextField()
    rsrv_type = models.CharField(max_length=10, verbose_name='적립유형')
    rsrv_type_nm = models.TextField()
    save_trm = models.IntegerField(verbose_name='저축기간')
    intr_rate = models.FloatField(verbose_name='최저금리')
    intr_rate2 = models.FloatField(verbose_name='최고금리')

    class Meta:
        verbose_name = "상품 상세 정보"
        verbose_name_plural = "상품 정보"
    

class UserSaving(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank = models.CharField(max_length=50)
    product = models.TextField()
    mtrt = models.FloatField()          # 만기후 이자율
    join_deny = models.IntegerField()   # {1:제한없음``, 3:일부제한}
    join_member = models.TextField()    # 1이 아닐때만 null=True
    max_limit = models.FloatField()     # 최대한도
    intr = models.FloatField()          # 본인이자율
    intr_rate_type = models.CharField(max_length=10, verbose_name='금리 유형')   # 금리유형/ 단리복리
    rsrv_type = models.CharField(max_length=10, verbose_name='적립유형')        # 적립 유형/ 자유형, 정액형  


class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    savings_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    pass