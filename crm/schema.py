import graphene
from graphene_django import DjangoObjectType
from graphene import Mutation, List, Field
from .models import *
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError


class CRMQuery(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

class CustomerType(DjangoObjectType):
    class Meta:
        model= Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model= Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model= Order
        fields = "__all__"


class OrderItemType(DjangoObjectType):
    class Meta:
        model= OrderItem
        fields = "__all__"


class PaymentType(DjangoObjectType):
    class Meta:
        model= Payment
        fields = "__all__"



class CreateCustomer(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        email=graphene.String(required=True)
        phone=graphene.String(required=True)

    customer = graphene.Field(CustomerType)


    @classmethod
    def mutate(cls, root, info, name, email, phone):

        if Customer.objects.filter(email=email).exists():
            raise Exception("A customer with this email already exists")
        
        if not phone.isdigit() or len(phone) < 10:
            raise Exception("Invalid phone Number. Must be at least 10")
        
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()

        return CreateCustomer(customer=customer)
    
class CustomerErrorType(graphene.ObjectType):
    index = graphene.Int()
    field = graphene.String()
    message = graphene.String()


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()
    address = graphene.String()
    company = graphene.String()
    
class BulkCreateCustomers(Mutation):
    class Arguments:
        customers = List(CustomerInput, required=True)

    created_customers = List(CustomerType)
    errors = List(CustomerErrorType)

    @classmethod
    def mutate(cls, root, info, customers):
        created = []
        errors = []

        for index, data in enumerate(customers):
            try:
                customer = Customer(**data)
                customer.full_clean()
                customer.save()
                created.append(customer)
            except ValidationError as e:
                for field, messages in e.message_dict.items():
                    for message in messages:
                        errors.append(CustomerErrorType(
                            index=index,
                            field=field,
                            message=message
                        ))
            except IntegrityError as e:
                errors.append(CustomerErrorType(
                    index=index,
                    field="email",
                    message="Email must be unique"
                ))
            except Exception as e:
                errors.append(CustomerErrorType(
                    index=index,
                    field="non_field_error",
                    message=str(e)
                ))

        return BulkCreateCustomers(created_customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        price=graphene.String(required=True)
        stock=graphene.String(required=True)

    product=graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, name, price, stock):
        product = Customer(name=name, price=price, stock=stock)
        product.save()

        return CreateCustomer(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        custom_id=graphene.String(required=True)
        product_id=graphene.String(required=True)
        order_date=graphene.String(required=True)

    
    order=graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, custom_id, product_id, order_date):
        order = Customer(custom_id=custom_id, product_id=product_id, order_date=order_date)
        order.save()

        return CreateCustomer(order=order)



class Query(graphene.ObjectType):
    customers=graphene.List(CustomerType)
    products=graphene.List(ProductType)
    orders=graphene.List(OrderType)
    payments=graphene.List(PaymentType)

    # customer = graphene.Object()

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()
    
    def resolve_orders(root, info):
        return Order.objects.all()
    
    def resolve_payments(root, info):
        return Payment.objects.all()
        # return "Hello World"

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field() 



schema = graphene.Schema(query=Query, mutation= Mutation)