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