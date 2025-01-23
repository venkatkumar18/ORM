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
    