# LBMS

## TODO

- django related field name (children) https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.related_name
- read about django reusable apps (https://docs.djangoproject.com/en/3.2/intro/reusable-apps/) and make changes
- Turn on dev environment on Heroku. Check that it uses a different db.
- Date format of Expenses (visible in expense list, it comes from model __str__ method)
- Make init_lbms modular:
  - Users group creation
  - Family lbms_group creation
- Sort expenses by date in expense list
- ALLOWED_HOSTS ?
- Review public code and consider keeping heroku deployment private (in a separate repo)
