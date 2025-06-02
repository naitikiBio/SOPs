### Ingesting Structured EHR Data
Version 1.0 Effective Data: 6/2/2025 Author: Naitik Shah

1.  #### Purpose
To define the standard procedures for ingesting structured Electronic Health Record (EHR) data using Fast Healthcare Interoperability Resources (FHIR) standards and Python. This SOP aims to ensure the integrity, security, and confidentiality of Protected Health Information (PHI) in compliance with the Health Insurance Portability and Accountability Act (HIPAA) regulations, including specific considerations for Google Cloud Platform (GCP) environments.

2. #### Scope
This SOP applies to all personnel, systems, and processes involved in the planning, development, execution, and maintenance of structured EHR data ingestion within the organization.

3. #### Definitions
	- **EHR**: Electronic Health Record - A digital version of a patient's paper chart.
	- **FHIR**: Fast Healthcare Interoperability Resources - A standard describing data formats and elements (known as "resources") and an Application Programming Interface (API) for exchanging electronic health records.
	- **PHI**: Protected Health Information - Individually identifiable health information that is transmitted or maintained in any form or medium (electronic, oral, or paper) by a covered entity or its business associates.
	- **HIPAA**: Health Insurance Portability and Accountability Act of 1996 - A US federal law designed to provide privacy standards to protect patients' medical records and other health information.

4. #### Procedures
4.1. **Data Identification and Understanding FHIR Data Types**
	1. **Identify Source Systems**:
		- Document the source EHR systems from which data will be ingested.
		- Determine the capabilities of source systems to export data in FHIR format or other structured formats that can be transformed into FHIR.
