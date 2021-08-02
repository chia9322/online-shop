price_id = []
product_id = 0
for product in products_db:
    product_id +=1
    new_product = stripe.Product.create(
      name=product.name,
        id=f'kuma_{product_id}',
        images=[product.img_url]
    )
    new_price = stripe.Price.create(
        product=f'kuma_{product_id}',
        currency='jpy',
        unit_amount=product.price
    )
    print(new_product)
    print(new_price)
    price_id.append(new_price.id)

print(price_id)


from product_database import products_db, ProductModel
# db.create_all()
#
# for product in products_db:
#     new_product = Product(
#         name=product.name,
#         price=product.price,
#         img=product.img,
#         number_of_img=int(product.number_of_img[0]),
#         category=product.category,
#         description=product.description
#     )
#     db.session.add(new_product)
#     db.session.commit()
#
# price_ids = ['price_1JJuxHElQsFHRZU3cTGMF9M6', 'price_1JJuxIElQsFHRZU341XHAgy2', 'price_1JJuxJElQsFHRZU3HiZZBMPX', 'price_1JJuxJElQsFHRZU3Kc37gcTi', 'price_1JJuxKElQsFHRZU3o28ge5Ec']
# for i in range(0, len(price_ids)):
#     product = db.session.query(Product).get(i+1)
#     product.price_id = price_ids[i]
#     db.session.commit()