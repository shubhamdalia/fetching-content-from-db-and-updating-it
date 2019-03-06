@app.route("/newimports/compare-products/", methods=['GET', 'POST'])
def compare_products():
    engine=util.get_query_engine()
    if request.method=='POST':
        productsids1=request.form.get('productsids1')
        click=request.form.get('click')
        query=""
        if click=='Similar':
            query="update wecat.sku_ref_to_sku set is_approved=1 where id="+productsids1
        else:
            query="update wecat.sku_ref_to_sku set is_approved=0 where id="+productsids1
        sql(engine,query)


    query="""select * from wecat.sku_ref_to_sku where is_approved is null limit 1;"""
    products=sql(engine,query).dicts()
    product_one=''
    first_product=''
    import json
    for product in products:
        product_one=product['sku_data']
        first_product = product['id_product']
        first_id= product['id']

    product_one=product_one.replace("u'","").replace("}'","}")
    product_one=json.loads(product_one)
    product_one_keys=product_one.keys()
    first_product = str(first_product)
    product_two = []
    data = {}
    with engine.begin() as conn:
        data['conn'] = conn
        data['id_product'] = first_product
        product_two = models.Product.get_product(**data) 
    product_two_keys=product_two.keys() 
    variable = '1'
    common_keys= []
    for a in product_one_keys:
        for b in product_two_keys:
             if a==b:
                common_keys.append(a)


    return render_template('newimport/compare_products.html', product=products, product_one=product_one, product_one_keys=product_one_keys, product_two=product_two, product_two_keys=product_two_keys,first_id=first_id,variable=variable,common_keys=common_keys)    