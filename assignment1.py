from abc import ABC,abstractmethod
class Paymentmethod(ABC):
    @abstractmethod
    def get_details(self):
        pass
    @abstractmethod
    def pay(self,amount):
        pass
class Razorpaycardpayment(Paymentmethod):
        def __init__(self,card_number):
            self.card_number=card_number
        def get_details(self):
            return self.card_number
        def pay(self,amount):
            print("Payment of",amount,"made using Razorpay Card")
            return True
class RazorpayUPIpayment(Paymentmethod):
     def __init__(self,upi_id):
          self.upi_id = upi_id
     def get_details(self):
          return self.upi_id
     def pay(self,amount):
          print("Payment of",amount,"made using Razorpay UPI")
          return True
class Stripecardpayment(Paymentmethod):
     def __init__(self,card_number):
          self.card_number=card_number
     def get_details(self):
          return self.card_number
     def pay(self,amount):
          print("Payment of",amount,"made using Stripe Card")
          return True
class StripeUPIpayment(Paymentmethod):
     def __init__(self,upi_id):
          self.upi_id=upi_id
     def get_details(self):
          return self.upi_id
     def pay(self,amount):
          print("Payment of",amount,"made using Stripe UPI")
          return True
class Factorypaymentmethod(ABC):
     factory={} 
     @classmethod
     def get_payment_object(cls,method_type,**kwargs):
          if method_type not in cls.factory:
               raise ValueError("Invalid payment method")
          return cls.factory[method_type](**kwargs)
class Razorpayfactory(Factorypaymentmethod):

    factory = {
        "card": Razorpaycardpayment,
        "upi": RazorpayUPIpayment
    }


class StripeFactory(Factorypaymentmethod):

    factory = {
        "card": Stripecardpayment,
        "upi": StripeUPIpayment
    }


class Aggregator(ABC):

    def __init__(self, name, processing_fee):
        self.name = name
        self.processing_fee = processing_fee

    @abstractmethod
    def call_get_payment_object(self, method_type, amount, **kwargs):
        pass


class RazorpayAggregator(Aggregator):

    def __init__(self):
        super().__init__("Razorpay", 2.0)

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment = Razorpayfactory.get_payment_object(
            method_type, **kwargs
        )

        print("Processing through Razorpay")
        print("Processing fee:", self.processing_fee, "%")

        return payment.pay(amount)


class StripeAggregator(Aggregator):

    def __init__(self):
        super().__init__("Stripe", 2.9)

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment = StripeFactory.get_payment_object(
            method_type, **kwargs
        )

        print("Processing through Stripe")
        print("Processing fee:", self.processing_fee, "%")

        return payment.pay(amount)


class AggregatorFactory:

    factory = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator
    }

    @classmethod
    def register_aggregator(cls, name, aggregator):
        cls.factory[name] = aggregator

    @classmethod
    def get_aggregator_object(cls, aggregator_name):
        if aggregator_name not in cls.factory:
            raise ValueError("Invalid aggregator")

        return cls.factory[aggregator_name]()


def main():

    print("Multi-Gateway Payment Processing")
    print()

    try:
        aggregator_name = input(
            "Select gateway (stripe/razorpay): "
        ).lower()

        aggregator = AggregatorFactory.get_aggregator_object(
            aggregator_name
        )

        method_type = input(
            "Select payment method (card/upi): "
        ).lower()

        if method_type == "card":

            card_number = input("Enter card number: ")
            amount = float(input("Enter amount: "))

            result = aggregator.call_get_payment_object(
                method_type,
                amount,
                card_number=card_number
            )

        elif method_type == "upi":

            upi_id = input("Enter UPI ID: ")
            amount = float(input("Enter amount: "))

            result = aggregator.call_get_payment_object(
                method_type,
                amount,
                upi_id=upi_id
            )

        else:
            print("Invalid payment method")
            return

        if result:
            print("Payment successful")
        else:
            print("Payment failed")

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":
    main()