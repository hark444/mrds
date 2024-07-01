from admin_app.models import Coupons


class CouponService():

    ######## Coupons #############
    def get_all_coupons(self, where={}):
        # return Coupons.objects.all().get(is_active=1)
        result = Coupons.objects.all().filter(**where)
        print(result.query)
        return result

    def get_coupon(self, where={}):
        try:
            coupon = Coupons.objects.get(**where)
            if coupon:
                return coupon

        except Coupons.DoesNotExist:
            return False


    def add_coupon(self, data={}):
        Obj = Coupons(**data)
        Obj.save()
        return Coupons.objects.last().coupon_id

    # def update_coupon(self, data, where):
    #     obj, created = Coupons.objects.update_or_create(
    #         coupon_id=where['coupon_id'], is_active=data['is_active'],
    #         defaults=data,
    #     )

    def update_coupon(self,data, where):
        Coupons.objects.filter(coupon_id=where['coupon_id']).update(is_active=data['is_active'])
