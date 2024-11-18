# Why?
You might ask - why a separate package and not just shove everything into the `dags` folder of Airflow.

That works for development. However, we are running more and more business-critical work-flows on Airflow. In order to ensure business continuity and reduce the risk of errors, we need more reliable and maintainable building blocks.


- *Maintainability*: You can reuse the components across multiple DAGs.
- *Quality*: This repository aims to set a new standard in the internal Python eco-system, hence we ensure
    - ✨ High code-quality with aggressive linters and strict PR policies
    - ✒️  Well-documented public API and examples
    - 📦 Transparent release cycle
    - 🧪 High test coverage
- *Reusability*: You can reuse the components across multiple DAGs.


!!! warning "Versioning"
    The package follows semantic versioning. Breaking changes will occur unannounced before `v1.0.0`. After that all breaking changes will lead to bumping the major version number.

# Contact
The project is hosted at [github.com/dfds-data/dagcellent](https://github.com/dfds-data/dagcellent).

If you have a feature request, noticed a bug - it is best to open a new issue on that page.
