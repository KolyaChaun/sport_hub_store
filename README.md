# SPORT HUB STORE

## Overview

[SPORT HUB](https://teamchallenge-sport-store-frontend.vercel.app) is an e-commerce platform designed for hassle-free
shopping.

## Features

- **Product Catalogue**: Structure of presentation, search, sorting, product filters.
- **Shopping Cart and Checkout**: Adding, updating, deleting products from the shopping cart, and proceeding to
  checkout.
- **User Personal Account**: User registration, email confirmation, authorization, personal data management, and viewing
  order history for a specific period.
- **Admin Panel**: Interface for managing the store, adding products and categories, and handling users.
- **Integration with NOVA POST API**: Delivery options, including courier, branch, and parcel locker services.
- **Integration with LiqPay**: Payment by card and invoice generation for customers.

## Logo

![Logo](docs/logo.png)

## Tech Stack

[![Stack](https://skillicons.dev/icons?i=python,docker,postgres,django,gcp&theme=dark&perline=10)](https://skillicons.dev)

## Getting Started

### Clone the Repository

- Use GitHub Desktop or another Git client:

  ![Clone](docs/gitinstal.png)

### Environment Setup

- Ensure you have a `.env` file in the root directory.
- Use the provided `.env.example` file to structure and populate variables as per your requirements.

### Run the Application with Docker

- Ensure you have Docker installed [Install Docker](https://docs.docker.com/get-docker/).
- Build and run the application:

  ```bash
  docker compose up -d --build
  ```

### Database Migration

- Create initial migrations:

  ```bash
  docker compose exec api ./src/manage.py makemigrations
  ```
- Apply migrations:

  ```bash
  docker compose exec api ./src/manage.py migrate
  ```

### Install Dependencies

- This project uses [Poetry](https://python-poetry.org/).
- Install all required packages:

  ```bash
  poetry install
  ```
- Add new packages as needed:

  ```bash
  poetry add <package_name>
  ```

### Running Tests

- Start a shell in the app container:

  ```bash
  docker compose exec api bash
  ```
- Execute tests with pytest:

  ```bash
  poetry run pytest src
  ```

### API Documentation

- Access the OpenAPI schema:

  [Swagger UI](http://host:port/swagger/)

### Deployment

- This project is deployed on [Google Cloud Platform](https://cloud.google.com).

## Contributors

- [Vita Yushchyk](https://github.com/vitayushchyk)
- [Mykola Chaiun](https://github.com/KolyaChaun)
