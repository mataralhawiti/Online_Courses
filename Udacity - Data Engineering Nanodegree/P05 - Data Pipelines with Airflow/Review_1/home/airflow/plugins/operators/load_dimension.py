from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    insert_sql_template = """
    INSERT INTO {table}
    {insert_sql} ;
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id="",
                 table="",
                 insert_sql="",
                 
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id=redshift_conn_id
        self.table=table
        self.insert_sql=insert_sql

    def execute(self, context):
        self.log.info('LoadDimensionOperator Started')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))
        
        self.log.info("loading data from Redshift staging table to dim table")
        insert_sql_template_format = LoadDimensionOperator.insert_sql_template.format(
            table=self.table,
            insert_sql=self.insert_sql
        )
        
        redshift.run(insert_sql_template_format)
        
        