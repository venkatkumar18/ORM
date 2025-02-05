1) Foreign key field have a {reference_model}_id as their name. because it stores the id of the referenced model
2) Table name will be like appname_model name 
3) With django extensions, we can use 
    python manage.py runscript orm_query --> To execute the run method, same like management command.
    python manage.py shell_plus --print-sql  --> A shell which will print all the SQL query.
4) To print the sql query we can use
    from django.db import connection
    print(connection.queries)
5) 'objects' is a default manager to the model
6) When we have validators in the model field during .save() it will not be triggered, we need to run full_clean() method to check it before save().
7) queryset.update() is a bulk operation it will not call the .save() method so it not trigerr the pre and post save signals.
8) Prefetch related suitable for many to one (when related model is trying to access the foreign key of a child model). Select related is suitable for one to many (when child model is trying to access the fields of the foreign key model).
9) The Prefetch function is used to add some filters in the prefetched related model instead of getting all the entries matching the parent model id.
10) Annotates is used to add a new field, we can use the aggregrate function inside it which will create GROUP BY clause in SQL.
11) We can generate an ER diagram of our models using django-extensions package, with this command - python manage.py graph_models -a > er_diagram.dot. This will create a dot file in online check for dot file to image converter. This will give the ER diagram of our models. We can configure for specific model in settings.py file kindly check the docs for configuration.

*) ORM
    * Restaurant.objects.all()                            - ALL RECORDS
    * Restaurant.objects.first()                            - FIRST RECORD
    * Restaurant.objects.last()                            - LAST RECORD
    * Restaurant.objects.count()                            - TOTAL COUNT
    * Restaurant.objects.all()[:2]                            - LIMIT RECORD
    * rating = Rating.objects.create(
        user=user,
        restaurant=restaurant,
        rating=3
    )                                                - CREATE RECORD AND PASS THE MODEL INSTANCE FOR FOREIGN KEY
    * Rating.objects.filter(rating=3)                  - FILTER RECORDS
    * Rating.objects.filter(rating__lte=3)             - LOOKUPS LESS THAN OR EQUAL TO 
    * Rating.objects.filter(rating__gte=3)             - LOOKUPS GREATER THAN OR EQUAL TO
    * Rating.objects.first().restaurant.name           - ACCESSING FOREIGN KEY ATTRIBUTES VALUE
    * Rating.objects.exclude(rating=2)                 - NOT CONDITION IN WHERE CLASS
    * Restaurant.objects.first().rating_set.all()      - REVERSE RELATION, BY DEFAULT IT IS modelname_set WE      CAN CHANGE IT IN THE models.py FOREIGN KEY DEFINITION WITH "related_name" PARAMETER. HERE THE RATING_SET IS A MANAGER WE CAN PERFORM ALL THE OPERATION ABOVE IN IT SAME LIKE objects.

    * rating, creted = Rating.objects.get_or_create(
        restaurant=restaurant,
        user=user,
        rating=2
    )                                                - IT USES SELECT QUERY IF NO VALUE RETURNED THEN INSERT IT 

    * Restaurant.objects.filter(name__startswith="P").update(website='https://test.com')   - TO BULK UPDATE ALL THE RECORDS IN THE QUERYSET

    * Restaurant.objects.all().delete()             - TO DELETE THE QUERYSET, FOR FOREIGN KEYS IT WILL DO CASCADE AND SET NULL INITIALLY (CHILDREN TABLES) THEN DELETE THE ENTRY IN THE PARENT TABLE.
    
    * Restaurant.objects.filter(name__startswith='C').exists()  - RETURN BOOLEAN, BASED ON STARTSWITH LOOKUP.
    * Restaurant.objects.filter(restaurant_type__in=[chinese,italian,fastfood],longitude__gt=0)  - IN,GT,LT LOOKUPS.
    * Sale.objects.filter(income__range=(50,60))     - BETWEEN OPERATOR USING RANGE LOOKUP
    * Restaurant.objects.order_by('-name')           - DESC
      Restaurant.objects.order_by('name')            - ASC
      Restaurant.objects.order_by('name').reverse()  - DESC
      Restaurant.objects.order_by(Lower('name'))     - "from django.db.models.functions import Lower" WE CAN    PASS FUNTION DIRECTLY TO FIELDS, THIS CREATES A LOWER CONVERSION IN SQL.
    * Restaurant.objects.earliest('date_opened')     - GET THE ENTRY ASC LIMIT 1 OF THAT FIELD
      Restaurant.objects.latest('date_opened')       - GET THE ENTRY DESC LIMIT 1 OF THAT FIELD
                                    - WE CAN ADD THE DEFAULT ORDERING AND GET_LATEST_BY IN MODEL META
    * Rating.objects.filter(restaurant__name__startswith='C')  - FOREIGN KEY FIELD FILTER WITH LOOKUPS
      Sale.objects.filter(restaurant__restaurant_type="CH")    - FOREIGN KEY FIELD FILTER
                                    - THESE FOREIGN KEY FILTERS WILL HAVE A INNER JOIN QUERY TO LINK THE TABLES
    
    * Prefetch Related
        N+1 Problem - For each N recrods(restaurant) one query will be execcuted to get the rating. To get the restaurant.all() one query is executed. So it is N+1 query.

        Usual Query For 14 restaurant records (Total query executed - 15)
            restaurants = Restaurant.objects.all()
            for restaurant in restaurants:
                print(restaurant.name)
                for rat in restaurant.rating.all():
                    print(rat.rating)
                print()
        

        Optimized query using prefetch related (total query executed - 2) Uses Inner Join
            restaurant = Restaurant.objects.only('name').prefetch_related('rating')
            for restaurant in restaurants:
                print(restaurant.name)
                for rat in restaurant.rating.all():
                    print(rat.rating)
                print()
    * Select Related
        Usual Query for 100 sales record (Total query executed 101) 1 to get all sales and remainig 100 for getting restaurant name.
            sales = Sale.objects.all()
            for sale in sales:
                print(sale.restaurant.name, sale.income)
        
        Optimized query using select_related (Total query 1) Uses Left Outer Join
            sales = Sale.objects.only('income','restaurant__name').select_related('restaurant')
            for sale in sales:
                print(sale.restaurant.name, sale.income)
    * Prefetch
        WITHOUT PREFETCH (which will select all the matching sale and rating query based on restaurant id)
            restaurant = Restaurant.objects.prefetch_related('rating','sale').filter(rating__rating=5). \
                            annotate(total_income=Sum('sale__income'))
            for res in restaurant:
                print(res.name, res.total_income)
        
        WITH PREFETCH (PUT A WHERE CLAUSE IN SALES QUERY TO FILTER RECORDS BASED ON RESTAURANT ID AND DATETIME)
            month_ago = timezone.now() - timezone.timedelta(days=31)
            sales_qs = Prefetch('sale', Sale.objects.filter(datetime__gte=month_ago))
    
            restaurant = Restaurant.objects.prefetch_related('rating',sales_qs).filter(rating__rating=5) \
        .                   annotate(total_income=Sum('sale__income'))

    * M2M
        WE CAN CREATE M2M FIELD ON A TABLE, THIS WILL CREATE A JUNCTION TABLE WHICH HAS THE ID FIELD TWO FOREIGN KEYS OF THE RESPECTIVE MODELS. THIS TABLE WILL BE AUTOMATICALLY CREATED, IF WE WANT TO ADD SOME OTHER FIELDS THEN WE CAN SPECIFY 'THROUGH' IN THE M2M FIELD AND ADD A CLASS, KINDLY REFER StaffRestaurant CLASS. WITH StaffRestaurant WE CAN PERFORM ALL ORM OPERATION LIKE REGULAR TABLE.

        staff.restaurant.all()              - RETURNS ALL THE RESTAURANT ENTRY FOR THAT STAFF
        staff.restaurant.add(restaurant, through_defaults={'salary': 50})    - ADD A M2M ENTRY IN THE M2M TABLE.
        staff.restaurant.count()            - RETURNS THE TOTAL COUNT OF RESTAURANT FOR A STAFF
        staff.restaurant.set(Restaurant.objects.all()[:5], through_defaults={'salary': 78})     - INSERT                            MULTIPLE RECORDS WHEN GIVEN IN QUERYSET

        staff.restaurant.clear()            - DELETES ALL THE ENTRY IN THE JUNCTION TABLE FOR A STAFF
        staff.restaurant.remove(restaurant) - REMOVES A PARTICULAR RESTAURANT IN THE TABLE
        staff.restaurant.filter(restaurant_type=Restaurant.TypeChoices.CHINESE)     - FILTER RECORDS
        restaurant.staff_set.all()          - M2M FIELD WAS ADDED IN STAFF MODEL, SO WE ACCESSED IT DIRECTLY FOR RELATED MODEL WE CAN USE THE {model}_set TO ACCESS IT.

        WITHOUT PREFETCH (For 10 jobs, total queries = 21 (N*2 + 1))
            jobs = StaffRestaurant.objects.all()
            for job in jobs:
                print(job.staff.name, end='  -   ')
                print(job.restaurant.name)

        USING PREFETCH (For 10 jobs, total queries = 3)

            jobs = StaffRestaurant.objects.prefetch_related('staff','restaurant')
            for job in jobs:
                print(job.staff.name, end='  -   ')
                print(job.restaurant.name)
    
    *  Restaurant.objects.values('name', 'website')       - RETURNS DICTIONARY OF VALUES IN A LIST.
       Restaurant.objects.values(capital_name=Upper('name'))  - CAPITALIZE THE NAME FIELD
       Restaurant.objects.values('rating__rating')      - WE CAN USE RELATED MODEL FIELD ALSO IN VALUES.
       Restaurant.objects.values_list('name',flat=True) - VALUES_LIST WILL RETURN THE RESULT IN LIST OF TUPLES IF WE SPECIFY ONLY ONE FIELD THEN WE CAN USE FLAT OPTION TO RETURN IT A SINGLE LIST WITH ALL VALUES.

       Restaurant.objects.aggregate(unique_hotels=Count('name'))    - AGGREGATE FUNCTION COUNT
       Sale.objects.annotate(min=Min('income'), 
        max=Max('income'),
        avg=Avg('income'),
        sum=Sum('income')).values('min','max','avg','sum')      - GROUP AGGREGATE FUNCTIONS.
    
       Restaurant.objects.annotate(name_length=Length('name')).filter(name_length__gte=10).order_by('-name_length')         - ANNOTATE WILL ADD A FIELD TO EVERY INSTANCE, WE CAN ACCESS IT, WE CAN USER THE ANNOTATED FIELD IN FILTER AND IN ORDER_BY CLAUSE. 

       concatenation_format = Concat('name',Value(' : [Rating '), 'rating__rating', Value(']'), output_field=CharField())
       restaurant = Restaurant.objects.annotate(message=concatenation_format)       - WE CAN CREATE A FORMAT OF MESSAGE USING CONCAT AND USING IT IN ANNOTATE


       Restaurant.objects.annotate(sum=Sum('sale__income')).values('name','sum')    - USING ANNOTATE WILL CREATE A "CAST(SUM("core_sale"."income") AS NUMERIC) AS "sum" QUERY AND FORM A GROUP BY CLAUSE WITH ALL THE FIELDS IN RESTAURANT MODEL.

       Restaurant.objects.values('name').annotate(sum=Sum('sale__income')).filter(sum__gte=500)     - USING ANNOTATE AFTER VALUE WILL FORM A GROUP BY CLAUSE ONLY ON THAT FIELD, AND USING FILTER WILL CREATE HAVING CLAUSE.

        Restaurant.objects.annotate(sum=Sum('sale__income')).values('sum')
        restaurant.aggregate(output=Avg('sum'))     - WE CAN AGGREGATE THE VALUE FROM A ANNOTATED FIELD.
    
    * F and Q expressions

        Rating.objects.first()
        rating.rating = F('rating') + 1
        rating.save()     - WE WILL SPECIFY THE FIELD AND DO OPERATION ON IT IN SQL, THE VALUE WILL NOT BE PULLED IN PYTHON MEMORY

        Rating.objects.update(rating=F('rating') * 2)       - UPDATES ALL THE RATING * 2
        sales = Sale.objects.all()
        for sale in sales:
            sale.expenditure = random.uniform(5,100)
        Sale.objects.bulk_update(sales, ['expenditure'])    - BULK UPDATE ALL THE SALES MODEL IN A SINGLE QUERY
        Sale.objects.filter(income__gte=F('expenditure'))   - USING F EXPRESSION IN FILTER QUERY
        Sale.objects.annotate(profit=F('income') - F('expenditure'))    - USING F IN ANNOTATE
        
        Sale.objects.aggregate(
        profit=Count('id', filter=Q(income__gt=F('expenditure'))),
        loss=Count('id', filter=Q(income__lt=F('expenditure')))
        )       - USING F IN AGGREGATE, THIS WILL GIVE THE TOTAL NUMBER OF PROFIT AND LOSS COUNTS.


        rating = Rating.objects.first()
        print(rating.rating)
        rating.rating = F('rating') + 1
        rating.save()
        
        print(rating.rating)
        rating.refresh_from_db()
        print(rating.rating)            - OUTPUT --> 2, F(rating) + Value(1) ,3. REFRESHING IT WILL GET THE VALUE IN PYTHON MEMORY.


        type_filter = Q(restaurant_type=it) | Q(restaurant_type=me)
        recently_opened = ~Q(date_opened__gte=timezone.now() - timezone.timedelta(days=40))
        restaurant = Restaurant.objects.filter(type_filter & recently_opened)       - WE CAN SPECIFY AND, NOT, NOT CONDITION IN THE FILTER EXPRESSION. USING | & ~ ON Q EXPRESSIONS.


        name_filter = Q(restaurant__name__regex='[0-9]+')
        profit_filter = Q(income__gt=F('expenditure'))
        sales = Sale.objects.select_related('restaurant').filter(name_filter | profit_filter)   - COMBINE AND, OR CONDITION USIN Q EXPRESSION.
    
    * COALESCE
        Restaurant.objects.filter(capacity__isnull=False)       - FILTER BY ISNULL LOOKUP
        Restaurant.objects.aggregate(total_sum=Coalesce(Sum(F('capacity')), 0))     - WILL RETURN NON NULL VALUE IF THE SUM IS NONE THEN WILL RETURN THE DEFAULT VALUE 0.

        Restaurant.objects.aggregate(total_sum=Sum(F('capacity'), default=0.0))     - WE CAN REPLICATE THE SAME BEHAVIOR USING DEFAULT PARAM TO RETURN NON NULL VALUE. BUT THE SQL WILL USE COALESCE ONLY IN THE BACKGROUND.

        Restaurant.objects.annotate(name_param=Coalesce(F('nickname'), F('name'))).values_list('name_param', flat=True)         - IT WILL RETURN NICKNAME PARAM OR ELSE WILL RETURN NAME PARAM.

    * IF/ELSE CONDITIONAL STATEMENTS

        it = Restaurant.TypeChoices.ITALIAN
        restaurant = Restaurant.objects.annotate(
            is_italian=Case(
                When(restaurant_type=it, then=True),
                default=False
            )
        )
        restaurant.filter(is_italian=True)      - WE CAN ADD MULTIPLE IF/ELSE CONDITION AND ASSIGN IT TO A VARIABLE USING ANNOTATE AND WE CAN FILTER IT BY THE RESULT.

        sales = Restaurant.objects.annotate(nsales=Count('sale__id'))
        sales = sales.annotate(popular=Case(
            When(nsales__gte=10, then=True),
            default=False
        )).values('nsales','popular')
        print(sales.filter(popular=True))       - ANOTHER EXAMPLE OF USING TWO ANNOTATES.


        restaurant = Restaurant.objects.annotate(
        avg=Avg('rating__rating'),
        total=Count('rating__id')
        )
        restaurant = restaurant.annotate(
            rating_bucket=Case(
                When(avg__gt=3.5, total__gt=1, then=Value("High Rated")),
                When(avg__range=(2,3.5), total__gt=1, then=Value("Average Rated")),
                When(avg__lt=2.5, then=Value('Low Rated'))
            )
        ).values('name','avg','total','rating_bucket')      - WE CAN HAVE MULTIPLE CONDITION AND FRAME A VALUE FOR THE RESULT AND WE CAN FILTER IT BASED ON THAT.



        types = Restaurant.TypeChoices
        asian = Q(restaurant_type=types.CHINESE) | Q(restaurant_type=types.INDIAN)
        europe = Q(restaurant_type=types.GREEK) | Q(restaurant_type=types.ITALIAN)
        na = Q(restaurant_type=types.MEXICAN)
        
        restaurant = Restaurant.objects.annotate(
            continent=Case(
                When(asian, then=Value('Asian')),
                When(europe, then=Value('Europe')),
                When(na, then=Value("North America")),
                default=Value("Not Available")
            )
        ).values('name','restaurant_type','continent')      - TO ADD A CONTINENT DATA BASED ON RESTAURANT TYPE


        dates = []
        first_date = Sale.objects.aggregate(Min=Min('datetime'))['Min']
        last_date = Sale.objects.aggregate(Max=Max('datetime'))['Max']
        count = itertools.count()
        while (dt := first_date + timezone.timedelta(days=10 * next(count)) ) <= last_date:
            dates.append(dt)
        whens = [
            When(datetime__range=(dt, dt + timezone.timedelta(days=10)), then=Value(dt.date()))
            for dt in dates
        ]
        cases = Case(
            *whens,
            output_field=CharField()
        )
        sales = Sale.objects.annotate(
            daterange=cases
        ).values('daterange').annotate(total_sales=Sum('income'))
            
        print(sales)            - TO GET THE TOTAL SALES FOR EVERY 10 DAYS FROM FIRST SALE TO LAST SALE

    
    * Subquery, OuterRef, Exists.
        IN WHERE CONDITION WHEN WE PUT A BRACKET () AND INCLUDE ANOTHER SQL CONDITION INSIDE IT IS CALLED AS SUBQUERY.

          restaurant = Restaurant.objects.filter(restaurant_type__in=[italian, chinese])
          Sale.objects.filter(restaurant__in=Subquery(restaurant.values('pk'))).count()  -  IN SALES TABLE      WHERE CONDITION A (A SQL CONDITION WILL EXECUTED TO GIVE THE IDS OF THE RESTAURANT). THIS IS EQUIVALENT TO THIS QUERY - Sale.objects.filter(restaurant__restaurant_type__in=[italian,chinese]) BUT THIS QUERY WILL FORM A JOIN.

        sale = Sale.objects.filter(restaurant_id=OuterRef('pk')).order_by('-datetime')
        restaurant = Restaurant.objects.annotate(
            last_sale=Subquery(sale.values('income')[:1]),
            last_expenditure=Subquery(sale.values('expenditure')[:1]),
            profit= F('last_sale') - F('last_expenditure')
        ).values('name','last_sale', 'last_expenditure', 'profit').order_by('id')     -  THIS CODE MEANING IS IN SELECT QUERY ITSELF WE ARE REFERRING THE FROM TABLES PROPERTY. 
        SAMPLE SQL EQUIVALENT IS 
        SELECT name, 
        (select income FROM core_sale where restaurant_id = core_restaurant.id order by datetime DESC LIMIT 1) AS last_sale  
        FROM core_restaurant
        SO FOR EVERY RESTAURANT RECORD THIS SUBQUERY NEED TO BE EXECUTED TO GET THE RESULT. 
            
        sale = Sale.objects.filter(restaurant_id=OuterRef('id'), income__gt=85)
        restaurant = Restaurant.objects.filter(Exists(sale))        - WE CAN USE EXISTS IN PLACE FOR SUBQUERY IT RETURN BOOLEAN VALUE FOR THE CONDITION AND RETURNS ONLY THE RESTAURANT THAT MATCHES THE CONDITION.


    * Transactions
        DJANGO WORKS IN AUTO COMMIT MODE, WHENEVER A ORM QUERIES ARE EXECUTED IT WILL BE COMMITTED IN A DATABASE, BUT IN SOME CASE WE HAVE DEPENDENCIES BETWEEN TWO MODELS, LIKE IF WE SAVE A MODEL SOME OPERATION NEED TO BE PERFORMED IN THE OTHER MODEL, IF EXCEPTION IS RAISED THE SECOND MODEL SAVE IS CANCELED BUT THE FIRST SAVE IS COMMITTED IN DB WE WANT TO RESTRICT IT.

        WITHOUT EXCEPTION:
            product1 = Product.objects.get(name='Book')
            order = Order.objects.create(product=product1, no_of_items=3)
            product1.number_of_stock -= order.no_of_items
            product1.save()

        WITH EXCEPTION:
            product1 = Product.objects.get(name='Book')
            order = Order.objects.create(product=product1, no_of_items=3)
            raise Exception("raised after save operation")
            product1.number_of_stock -= order.no_of_items
            product1.save()     - HERE ORDER WILL BE SAVED BUT THE PRODUCT WILL NOT BE SAVED, ONE CHANGE IS HERE NUMBER_OF_STOCK IS POSITVE FIELD BUT WHEN WE SUBTRACT IF IT IS NEGATIVE THEN IT WILL RAISE AN EXCEPTION.
        
        SOLUTION:
            with transaction.atomic():
                product1 = Product.objects.get(name='Book')
                order = Order.objects.create(product=product1, no_of_items=3)
                
                raise Exception("raised after save operation")
                product1.number_of_stock -= order.no_of_items
                product1.save()     - THIS CODE WILL NOT ALLOW ORDER TO BE SAVED IN DATABASE ONLY AT THE END OF THE TRANSACTION THE COMMIT WILL OCCUR. IF EXCEPTION OR SYSTEM CRASH OCCURS THEN ALL THE CHANGE WILL BE ROLLBACKED. IT WILL CREATE A "BEGIN" AND AT THE END WILL HAVE A "COMMIT" SQL STATEMENTS
            
        on_commit:
            with transaction.atomic():
                product1 = Product.objects.get(name='Book')
                order = Order.objects.create(product=product1, no_of_items=4)
                product1.number_of_stock -= order.no_of_items
                product1.save()
            transaction.on_commit(success_method)       - ONLY WHEN THE TRANSACTION IS SUCCESS THE ON_COMMIT PARAM METHOD WILL BE EXECUTED.

        select_for_update():
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=1)  
            
            - THIS WILL LOCK THIS PARTICULAR ROW TILL THE END OF THE TRANSACTION, THE OTHER CALLS CAN ABLE TO READ THIS PRODUCT BUT CAN'T MODIFY IT, THIS WILL FIX CONCURRENCY ISSUES WHEN MULTIPLE CALLS UPDATE THE SAME RECORD.
            
    * Content-Type
        content_type = ContentType.objects.get(app_label='core', model='restaurant')
        dynamic_model = content_type.model_class()
        dynamic_entry = content_type.get_object_for_this_type(name='Bombay Bustle')
        content_type_model = ContentType.objects.get_for_model(Restaurant)
        print(dynamic_entry)        - THIS PRINTS THE RESTAURANT ENTRY
        print(dynamic_model.objects.first())        - THIS WILL PRINT ALL THE ENTRIES IN THE RESTAURANT MODEL.
        print(content_type_model.app_label, content_type_model.model)   - WITH A MODEL CLASS WE CAN GET THE CONTENT TYPE MODEL INSTANCE OF IT.

    * Generic Foreign Key
        WHEN WE WANT A SINGLE FOREIGN KEY AND REFERENCE MULTIPLE MODELS, THEN WE CAN USE GENERIC FOREIGN KEY, REFER COMMENTS MODEL, OVER THERE WE HAVE ADDED content_type,object_id,content_object field, HERE CONTENT_TYPE WILL STORE THE django_content_type ID OF THE MODEL, OBJECT_ID WILL THE INSTANCE UNIQUE ID AND CONTENT OBJECT WE CAN GET THE REFERRED MODULE INSTANCE ITSELF.

            comments = Comment.objects.first()
            print(comments)     
            print(comments.content_object.name)     - RESTAUTANY NAME
            print(comments.content_type)            - CORE | RESTAURANT
        
            restaurant = Restaurant.objects.first()
            c1 = Comment.objects.create(
                text="This Restaurant special is MysorePark",
                content_object=restaurant
            )       - WE CAN ADD A COMMENT TO A RESTAURANT BY SPECIFYING ONLY THE CONTENT_OBJECT.

            restaurant = Restaurant.objects.first()
            print(restaurant.comments.all())
            print(restaurant.comments.count())
            restaurant.comments.add(
                Comment.objects.create(text='Great Customer Service', content_object=restaurant)
            )
            comment = Comment.objects.filter(
                restaurant__restaurant_type=Restaurant.TypeChoices.INDIAN)
            print(comment)    - AFTER ADDING GENERIC RELATION AND RELATED_QUERY_NAME IN RESTAURANT AND IN RAITNG MODEL WE CAN ACCESS PARENT AND CHILD FIELD IN THIS WAY.
    * CONSTRAINTS 
        WE CAN ADD UNIQUE,NOT NULL, CHECK CONSTRAINT TO FIELDS OF A MODEL TO PREVENT IT FROM SAVING. 
    