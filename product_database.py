class ProductModel:

    def __init__(self, name, price, img, number_of_img, category, description, img_url):
        self.name = name
        self.price = price
        self.img = img
        self.number_of_img = number_of_img,
        self.category = category
        self.description = description
        self.img_url = img_url


products_db = [
    ProductModel(
        name='ロールペーパーカバー',
        price=2200,
        img='toilet-paper-cover',
        number_of_img=5,
        category='チャイロイコグマ',
        description='シックなカフェカラーが大人っぽいチャイロイコグマのロールペーパーカバーができました☆ブラックのリボンがついていたり、裏にはクマ型のはちみつの刺繍が入っていたりこだわりポイントがたくさん♪チャイロイコグマでおうちのトイレを癒しの空間にしてみませんか？ ',
        img_url='https://shop.san-x.co.jp/img2/RLK/RLK8792_L.jpg'
    ),
    ProductModel(
        name='ウェルカムドール',
        price=8580,
        img='wedding-doll',
        number_of_img=5,
        category='チャイロイコグマ,コリラックマ',
        description='大人気のウェルカムドールが、2020年バージョンで登場です。初登場のチャイロイコグマとコリラックマが幸せな2人をお祝いします。',
        img_url='https://shop.san-x.co.jp/img2/RLK/RLK8072_L.jpg?200916'

    ),
    ProductModel(
        name='アオイコオオカミ',
        price=2530,
        img='aoikoookami',
        number_of_img=1,
        category='アオイコオオカミ,チャイロイコグマのお友達',
        description='チャイロイコグマデビュー5周年！華やかなチューリップとトレンドのピスタチオカラーを取り入れた、春にぴったりのデザインシリーズです。「チャイロイコグマのお友達」テーマです♪大きめの手足がとってもかわいいアオイコオオカミのぬいぐるみができました！ふわふわの胸毛とリボンがポイントだよ☆ほわほわな触り心地に癒される♪キュートすぎるアオイコオオカミにキュン…☆',
        img_url='https://shop.san-x.co.jp/img2/RLK/RLK8603_L.jpg'
    ),
    ProductModel(
        name='チューリップコグマ',
        price=2750,
        img='tulip-koguma',
        number_of_img=2,
        category='チャイロイコグマ',
        description='チャイロイコグマデビュー5周年！華やかなチューリップとトレンドのピスタチオカラーを取り入れた、春にぴったりのデザインシリーズです。「チャイロイコグマのお友達」テーマです♪チューリップをかかえた姿がかわいすぎるチューリップぬいぐるみです！チューリップを外すとスマートフォンをぎゅっと出来るよ☆耳にはくまんばちが付いているよ♪チャイロイコグマ好きさんにぜひお迎えして欲しい☆',
        img_url='https://shop.san-x.co.jp/img2/RLK/RLK8598_L.jpg'
    ),
    ProductModel(
        name='カフェカラー・リラックマ(S)',
        price=2200,
        img='rilakkuma-cafe',
        number_of_img=3,
        category='リラックマ',
        description='ちょこんとしたお座りポーズがかわいいリラックマのSサイズのぬいぐるみです。キャラメルみたいなかわいいカラーに癒される♪',
        img_url='https://shop.san-x.co.jp/img2/RLK/RLK7477_L.jpg'
    )
]
#
# db.create_all()
#
# for product in products_db:
#     new_product = Product(
#         name=product.name,
#         price=product.price,
#         img=product.img,
#         number_of_img=product.number_of_img,
#         category=product.category,
#         description=product.description
#     )
#     db.session.add(new_product)
#     db.session.commit()