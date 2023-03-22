# ECR Sounds Sorting based on [JKCSiteTemplate](https://github.com/JediKnightChan/JKCSiteTemplate)

## How it works

Fore more details about the template, refer to
original [repository](https://github.com/JediKnightChan/JKCSiteTemplate)

## Differences from the template

- Sign Up
- An app for sorting sounds (sending reviews about them)
- Using django-dbbackup along with celery for auto backup of the database to S3. Removing old backups is done on
  S3 level with lifecycle.
