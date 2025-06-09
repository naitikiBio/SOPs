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
   - Document the source EHR systems from which data will be ingested
   - Determine the capabilities of source systems to export data in FHIR format or other structured formats that can be transformed into FHIR.
2. **Understand Key FHIR Resources**:
   - FHIR organizes data into "Resources." Common resources relevant to EHR data ingestion include:
     - **Patient**: Demographic and administrative information about an individual receiving care.
       - _Key fields_: id, identifier (e.g., MRN), name, gender, birthDate, address, telecom (contact info), managingOrganization.
     - **Observation**: Measurements and simple assertions made about a patient.
       - _Key fields_: id, status, category, code (what is being observed, e.g., LOINC code for blood pressure), subject (reference to Patient), effectiveDateTime or effectivePeriod, value[x] (e.g., valueQuantity, valueCodeableConcept, valueString).
     - **Encounter**: An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.
       - _Key fields_: id, status, class, type, subject (reference to Patient), participant (involved practitioners), period.
     - **Condition**: A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.
       - _Key fields_: id, clinicalStatus, verificationStatus, category, code, subject (reference to Patient), onsetDateTime or onsetAge.
     - **MedicationRequest**: An order or request for both supply of the medication and the instructions for administration of the medication to a patient.
       - _Key fields_: id, status, intent, medicationCodeableConcept or medicationReference, subject (reference to Patient), authoredOn, requester.
   - Familiarize with the structure and common elements of these resources as defined in the official HL7 FHIR specification.

4.2 **Data Ingestion using Python and fhirclient**
1. **Set up Python Environment**:
   - Ensure a supported version of Python is installed. (If unsure how to, refer to this SOP: https://github.com/naitikiBio/SOPs/blob/main/Ingesting_Data_From_APIs.md)
   - Use virtual environments (e.g., venv, conda) to manage project dependencies.
2. **Install fhirclient library**:
   ```bash
   pip install fhirclient
   ```
3. **Connect to a FHIR Server**:
   - The fhirclient library facilitates interaction with FHIR servers.
   - Configuration settings include the FHIR server's base URL (api_base) and, if applicable, application identifiers (app_id).
   - **Example for an open FHIR server**:
     ```python
     from fhirclient import client

     settings = {
     	'app_id': 'my_ehr_ingestion_app',
     	'api_base': 'https://your-fhir-server-base-url/fhir' # Replace with actual FHIR server URL
     }
     smart = client.FHIRClient(settings = settings)
     ```
   - **For protected servers (requiring OAuth2 authentication)**:
     - The fhirclient supports SMART on FHIR authentication. This typically involves redirecting a user for authorization or using backend service authentication if supported by the FHIR server.
     - Refer to fhirclient documentation for detailed OAuth2 setup. Ensure secure handling of client credentials.
     - smart.prepare() can be used to check if authorization is needed. smart.ready indicates if the client is ready to make requests.
4. **Reading FHIR Resources**:
   - **Fetch a specific resource by ID**:
     ```python
     import fhirclient.models.patient as p
     try:
     	patient = p.Patient.read('patient_id_example', smart.server) # Replace 'patient_id_example'
     	print(patient.name[0].given)
     	# Process patient data
     except Exception as e:
     	print(f"Error reading patient: {e}")
     ```

   - **Search for resources**:
     ```python
     import fhirclient.models.observation as o
     try:
     	search = o.Observation.where(struct = {
     		'subject': 'Patient/patient_id_example', # Replace 'patient_id_example'
     		'code': 'http://lonic.org/8302-2' # Example: LONIC code for Body Height
     	})
     	observations = search.perform_resources(smart.server)
     	for obs in observations:
     		if obs.valueQuantity:
     			print(f"Observation: {obs.code.text}, Value: {obs.valueQuantity.value} {obs.valueQuantity.unit}")
     		# Process observation data
     except Exception as e:
     	print(f"Error searching observations: {e}")
5. **Creating/Updating FHIR Resources (if applicable to ingestion workflow)**:
   - While ingestion primarily involves reading, if the workflow requires creating or updating resources (e.g., transforming and storing data in a FHIR-compliant repository):
     ```python
     # Example: Creating a new patient resource (simplified)
     # Ensure all required fields are populated according to FHIR specs and profiles
     from fhirclient.models.humanname import HumanName
     from fhirclient.models.identifier import Identifier

     patient_data = {
     	"resourceType": "Patient",
     	"identifier": [{"system": "urn:ietf:rfc:3986", "value": "some_unique_id"}],
     	"name": [{"use": "official", "family": "Doe", "given": ["John"]}],
     	"gender": "male",
     	"birthDate": "1970-01-01"
     }
     new_patient = p.Patient(patient_data)
     try:
     	response = new_patient.create(smart.server)
     	print(f"Patient created with ID: {response.id}")
     except Exception as e:
     	print(f"Error creating patient: {e}")

   - Always validate resources against FHIR profiles before creation/update.
6. **Error Handling**:
   - Implement robust error handling (e.g., try-except blocks) for API requests, data parsing, and validation.
   - Log errors comprehensively, including timestamps, error messages, and relevant context (e.g., resource ID, query parameters).
   - Implement retry mechanisms for transient network errors, with exponential backoff.
#### 5.3. **PHI and HIPAA Compliance Considerations**
#### 5.3.1. **General Principles**
1. **Minimum Necessary Rule**: Access, use, and disclose only the minimum necessary PHI to accomplish the intended purpose of the data ingestion.
2. **Access Controls (RBAC)**:
   - Implement RBAC to ensure that only authorized personnel have access to PHI.
   - Permissions should be granted based on job roles and responsibilities.
   - Regularly review and update access permissions.
3. **Data Encryption**:
   - **At Rest**: All PHI stored in databases, file systems, or object storage must be encrypted using strong encryption algorithms (e.g., AES-256).
   - **In Transit**: All PHI transmitted over networks (internal or external) must be encrypted using secure protocols (e.g., TLS 1.2+). This includes data transfer between the EHR source, ingestion scripts, and storage systems.
4. **Audit Trails and Logging**:
   - Maintained detailed audit logs of all access, creation, modification, and deletion of PHI.
   - Logs should include user identification, date, time, and specific data accessed/modified.
   - Regularly review audit logs for suspicious activity.
5. **De-identification**:
   - If PHI is to be used for research, analytics, or other secondary purposes where direct identifiers are not needed, de-identify the data.
   - HIPAA provides two methods for de-identification:
     - **Safe Harbor**: Removal of 18 specific identifiers.
     - **Expert Determination**: A qualified statistician or expert determines that the risk of re-identification is very small.
   - Document the de-identification method used.
6. **Business Associate Agreements (BAAs)**:
   - Ensure a signed BAA is in place with all third-party vendors (including cloud service providers like Google) that will create, receive, maintain, or transmit PHI on behalf of the organization.
7. **Secure Storage and Transmission**:
   - Store PHI in secure, access-controlled environments.
   - Use secure methods for transmitting PHI (e.g., SFTP, VPN, HTTPS).
8. **Incident Response Plan**:
   - Develop and maintain an incident response plan to address potential breaches of PHI.
   - The plan should include procedures for detection, containment, eradication, recovery, and post-incident analysis, as well as breach notification procedures as per HIPAA.
9. **Employee Training**:
    - All personnel handling PHI must receive regular training on HIPAA requirements, PHI security, and organizational policies and procedures.
#### 5.3.2. **Technical Safeguards (as per HIPAA Security Rule)**
1. **Unique User Identification (Required)**: Assign a unique name and/or number for identifying and tracking user identity.
2. **Authentication (Required)**: Implement procedures to verify that a person or entity seeking access to PHI is the one claimed. This includes strong password policies and multi-factor authentication (MFA) where appropriate.
3. **Authorization Mechanisms (Required)**: Implement policies and procedures for granting access to PHI, such as through RBAC.
4. **Data Backup and Disaster Recovery (Required)**: Establish and implement procedures to create and maintain retrievable exact copies of PHI. Have a disaster recovery plan to restore any loss of data.
#### 5.4. GCP-specific Considerations for PHI and HIPAA
When using GCP for ingesting and storing EHR data:
1. **Business Associate Agreement (BAA) with Google Cloud**:
   - Ensure a BAA is executed with Google Cloud. This agreement outlines Google's responsibilities for protecting PHI.
   - Understand which GCP services are covered under the BAA ("HIPAA-eligible services").
2. **Utilize HIPAA-Eligible Services**:
   - Use only GCP services that are covered by the BAA for workloads involving PHI. Examples include:
     - Google Cloud Storage
     - Google BigQuery
     - Google Compute Engine
     - Google Kubernetes Engine (GKE)
     - Google Cloud Healthcare API
     - Cloud SQL
     - Cloud Logging & Cloud Monitoring
   - Refer to Google Cloud's documentation for the most up-to-date list of HIPAA-eligible services.
3. **Identity and Access Management (IAM)**:
   - Apply the **Principle of Least Privilege**: Grant users and service accounts only the permissions necessary to perform their tasks.
   - Use predefined IAM roles where possible, or create custom roles with granular permissions.
   - Utilize **service accounts** for applications and scripts that access GCP resources. Assign minimal necessary permissions to service accounts. Avoid using user credentials in scripts.
   - Regularly review IAM policies and audit access patterns.
   - Use **Workforce Identity Federation** or **Cloud Identity** for managing user identities.
4. **Data Encryption on GCP**:
   - **Encryption at Rest**: GCP encrypts data at rest by default.
