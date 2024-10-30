# Web Application that Uses Semantic Web Technologies and AI

This repository contains a web application that combines Semantic Web technologies and a custom-trained AI model for Named Entity Recognition (NER) to process data from the Carta ASE (Academia de Studii Economice). Developed as a bachelor’s thesis project, this application focuses on efficient data integration, advanced querying capabilities, and a user-friendly interface, making it easier to navigate and manage complex data.

---

## Project Overview

The primary objective of this project is to leverage Semantic Web technologies, coupled with a custom AI model, to enhance data accessibility and interoperability. The application enables machines to understand and process data contained in the Carta ASE, facilitating robust data integration and complex query execution. By using RDF (Resource Description Framework) and SPARQL queries, the application aims to offer accurate and context-sensitive responses to user queries.

---

## Features

- **User Authentication**: Secure login system utilizing PostgreSQL and JWT (JSON Web Token) for session management.
- **Semantic Data Management**: Data from Carta ASE is structured in RDF Turtle format and stored in an Apache Jena Fuseki server for efficient access and updating.
- **Custom AI NER Model**: A specially trained Named Entity Recognition (NER) model interprets user inputs accurately, enabling context-aware responses based on the Carta ASE data.
- **SPARQL Querying**: Dynamic SPARQL templates for executing complex, nested queries based on user input.
- **User-Friendly Interface**: Minimalistic design with a chatbot-style query input for ease of interaction.

---

## Technologies Used

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL for user management; Apache Jena Fuseki for RDF storage and SPARQL querying
- **NER System**: spaCy, with a custom-trained model and data augmentation using RoWordNet
- **Version Control**: GitHub for collaboration and version management

---

