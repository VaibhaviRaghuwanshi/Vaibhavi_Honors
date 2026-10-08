from abc import ABC, abstractmethod
#  Payment Methods 

class PaymentMethod(ABC):

    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass


class RazorpayCardPayment(PaymentMethod):

    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Razorpay Card - " + self.card_number[-4:]

    def pay(self, amount):
        print("Payment made using Razorpay Card")
        print("Amount:", amount)
        return True


class RazorpayUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return "Razorpay UPI - " + self.upi_id

    def pay(self, amount):
        print("Payment made using Razorpay UPI")
        print("Amount:", amount)
        return True


class StripeCardPayment(PaymentMethod):

    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Stripe Card - " + self.card_number[-4:]

    def pay(self, amount):
        print("Payment made using Stripe Card")
        print("Amount:", amount)
        return True


class StripeUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return "Stripe UPI - " + self.upi_id

    def pay(self, amount):
        print("Payment made using Stripe UPI")
        print("Amount:", amount)
        return True


#  Payment Method Factory 

class FactoryPaymentMethod(ABC):

    factory = {}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        method_type = method_type.lower()

        if method_type not in cls.factory:
            raise ValueError("Invalid payment method")

        return cls.factory[method_type](**kwargs)


class RazorpayFactory(FactoryPaymentMethod):

    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment
    }


class StripeFactory(FactoryPaymentMethod):

    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment
    }


#  Aggregator 

class Aggregator(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def call_get_payment_object(self, method_type, amount, **kwargs):
        pass


class RazorpayAggregator(Aggregator):

    processing_fee = 2.0

    def __init__(self):
        super().__init__("Razorpay")

    def call_get_payment_object(self, method_type, amount, **kwargs):

        payment = RazorpayFactory.get_payment_object(
            method_type, **kwargs
        )

        print("\nGateway:", self.name)
        print("Processing fee:", self.processing_fee, "%")
        print("Payment details:", payment.get_details())

        return payment.pay(amount)


class StripeAggregator(Aggregator):

    processing_fee = 2.9

    def __init__(self):
        super().__init__("Stripe")

    def call_get_payment_object(self, method_type, amount, **kwargs):

        payment = StripeFactory.get_payment_object(
            method_type, **kwargs
        )

        print("\nGateway:", self.name)
        print("Processing fee:", self.processing_fee, "%")
        print("Payment details:", payment.get_details())

        return payment.pay(amount)


#  Aggregator Factory 
class AggregatorFactory:

    factory = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name):

        aggregator_name = aggregator_name.lower()

        if aggregator_name not in cls.factory:
            raise ValueError("Invalid aggregator")

        return cls.factory[aggregator_name]()


#  Main Program 

print("===== PAYMENT PROCESSING SYSTEM =====")

try:

    aggregator_name = input(
        "Enter aggregator (stripe/razorpay): "
    ).lower()

    method_type = input(
        "Enter payment method (card/upi): "
    ).lower()

    amount = float(input("Enter amount: "))

    if amount <= 0:
        print("Amount should be greater than zero.")

    else:

        aggregator = AggregatorFactory.get_aggregator_object(
            aggregator_name
        )

        if method_type == "card":

            card_number = input("Enter card number: ")

            if len(card_number) < 4:
                print("Invalid card number.")

            else:
                result = aggregator.call_get_payment_object(
                    method_type,
                    amount,
                    card_number=card_number
                )

                if result:
                    print("Payment successful!")

        elif method_type == "upi":

            upi_id = input("Enter UPI ID: ")

            if upi_id == "":
                print("UPI ID cannot be empty.")

            else:
                result = aggregator.call_get_payment_object(
                    method_type,
                    amount,
                    upi_id=upi_id
                )

                if result:
                    print("Payment successful!")

        else:
            print("Invalid payment method.")

except ValueError as e:
    print("Error:", e)

except Exception as e:
    print("Something went wrong:", e)