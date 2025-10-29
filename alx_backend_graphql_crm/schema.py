

import graphene
from graphene_django import DjangoObjectType
from graphene import Mutation, List, Field, relay
from crm.models import *
from crm.models import Product
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from graphene_django.filter import DjangoFilterConnectionField
from crm.filters import CustomerFilter, ProductFilter, OrderFilter


class CRMQuery(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

class CustomerType(DjangoObjectType):
    class Meta:
        model= Customer
        fields = "__all__"
        interfaces = (relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model= Product
        fields = "__all__"
        interfaces = (relay.Node,)


class OrderType(DjangoObjectType):
    class Meta:
        model= Order
        fields = "__all__"
        interfaces = (relay.Node,)


class OrderItemType(DjangoObjectType):
    class Meta:
        model= OrderItem
        fields = "__all__"
        interfaces = (relay.Node,)


class PaymentType(DjangoObjectType):
    class Meta:
        model= Payment
        fields = "__all__"
        interfaces = (relay.Node,)



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

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)

        updated_products = []
        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_products.append(product)

        if not updated_products:
            message = "No low-stock products found."
        else:
            message = f"{len(updated_products)} products updated successfully."

        return UpdateLowStockProducts(
            message=message,
            updated_products=updated_products
        )


# class Query(graphene.ObjectType):
#     customers=graphene.List(CustomerType)
#     products=graphene.List(ProductType)
#     orders=graphene.List(OrderType)
#     payments=graphene.List(PaymentType)

#     # customer = graphene.Object()

#     def resolve_customers(root, info):
#         return Customer.objects.all()

#     def resolve_products(root, info):
#         return Product.objects.all()
    
#     def resolve_orders(root, info):
#         return Order.objects.all()
    
#     def resolve_payments(root, info):
#         return Payment.objects.all()
#         # return "Hello World"

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field() 


# crm/schema.py




# ---------------
# Query Class
# ---------------

class Query(graphene.ObjectType):

    hello = graphene.String(description="Simple heartbeat test field")

    def resolve_hello(root, info):
        return "CRM is alive and responding!"

    # Customers with filter + order_by
    all_customers = DjangoFilterConnectionField(
        CustomerType,
        filterset_class=CustomerFilter,
        order_by=graphene.List(of_type=graphene.String),
        description="List of customers with optional filtering and ordering."
    )

    # Products with filter + order_by
    all_products = DjangoFilterConnectionField(
        ProductType,
        filterset_class=ProductFilter,
        order_by=graphene.List(of_type=graphene.String),
        description="List of products with optional filtering and ordering."
    )

    # Orders with filter + order_by
    all_orders = DjangoFilterConnectionField(
        OrderType,
        filterset_class=OrderFilter,
        order_by=graphene.List(of_type=graphene.String),
        description="List of orders with optional filtering and ordering."
    )

    # Optional: override resolvers to apply order_by manually
    def resolve_all_customers(self, info, **kwargs):
        qs = Customer.objects.all()
        order_by = kwargs.get("order_by")
        if order_by:
            qs = qs.order_by(*order_by)

        return qs

    def resolve_all_products(self, info, **kwargs):
        qs = Product.objects.all()
        order_by = kwargs.get("order_by")
        if order_by:
            qs = qs.order_by(*order_by)

        return qs

    def resolve_all_orders(self, info, **kwargs):
        qs = Order.objects.all()
        order_by = kwargs.get("order_by")
        if order_by:
            qs = qs.order_by(*order_by)

        return qs

schema = graphene.Schema(query=Query, mutation=Mutation)
