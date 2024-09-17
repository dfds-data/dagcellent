# Dagcellent

Dagcellent is a library, which contains reusable components to work with Apache Airflow. It is designed to make the development of Airflow DAGs easier and more efficient.

Some of the features of Dagcellent are:
 
- **Dynamic DAGs**: Create DAGs dynamically.
- **DAG from config**: Create DAGs from a configuration file.


## Why?
You might ask - why a separate package and not just shove everything into the `dags` folder of Airflow.

We are running more and more business-critical work flows on Airflow. In order to ensure business continuity and reduce the risk of errors, we need more reliable and maintainable building blocks.


- *Maintainability*: You can reuse the components across multiple DAGs.
- *Quality*: This repository aims to set a new standard in the internal Python eco-system, hence we ensure
    - ✨ High code-quality with aggressive linters and strict PR policies
    - ✒️  Well-documented public API and examples
    - 📦 Transparent release cycle
    - 🧪 High test coverage
- *Reusability*: You can reuse the components across multiple DAGs.


