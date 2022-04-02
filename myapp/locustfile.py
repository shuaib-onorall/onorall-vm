from locust import HttpUser, task

class FirstLocust(HttpUser):
    
    @task
    def hello_world_1(self):
        self.client.get('comments')