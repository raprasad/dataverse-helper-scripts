	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

	@Column(nullable=false, unique=true)
	private String serviceName;

	private String serviceDescription;

	@Column( nullable=false )
	private String apiEndpointURL;

	private String apiUsername;

	private String apiEncryptedPassword;

	private String apiParameters;

	private String visualizationURL;

	private String exploreButtonURL;

	private boolean exploreButtonOpensNewWindow;

	@Column( nullable=false )
	@ValidateEmail(message = "Please enter a valid email address.")
	private String contactName;

	@Column( nullable=false )
	private String contactEmail;

	private boolean serviceActive;

	private String serviceInactiveMessage;

	private String serviceDownMessage;

	private Timestamp updated;

	private Timestamp created;


    /**
     *  Set id
     *  @param id
     */
    public void setId(Long id){
        this.id = id;
    }

    /**
     *  Get for id
     *  @return Long
     */
    public Long getId(){
        return this.id;
    }
    

    /**
     *  Set serviceName
     *  @param serviceName
     */
    public void setServiceName(String serviceName){
        this.serviceName = serviceName;
    }

    /**
     *  Get for serviceName
     *  @return String
     */
    public String getServiceName(){
        return this.serviceName;
    }
    

    /**
     *  Set serviceDescription
     *  @param serviceDescription
     */
    public void setServiceDescription(String serviceDescription){
        this.serviceDescription = serviceDescription;
    }

    /**
     *  Get for serviceDescription
     *  @return String
     */
    public String getServiceDescription(){
        return this.serviceDescription;
    }
    

    /**
     *  Set apiEndpointURL
     *  @param apiEndpointURL
     */
    public void setApiEndpointURL(String apiEndpointURL){
        this.apiEndpointURL = apiEndpointURL;
    }

    /**
     *  Get for apiEndpointURL
     *  @return String
     */
    public String getApiEndpointURL(){
        return this.apiEndpointURL;
    }
    

    /**
     *  Set apiUsername
     *  @param apiUsername
     */
    public void setApiUsername(String apiUsername){
        this.apiUsername = apiUsername;
    }

    /**
     *  Get for apiUsername
     *  @return String
     */
    public String getApiUsername(){
        return this.apiUsername;
    }
    

    /**
     *  Set apiEncryptedPassword
     *  @param apiEncryptedPassword
     */
    public void setApiEncryptedPassword(String apiEncryptedPassword){
        this.apiEncryptedPassword = apiEncryptedPassword;
    }

    /**
     *  Get for apiEncryptedPassword
     *  @return String
     */
    public String getApiEncryptedPassword(){
        return this.apiEncryptedPassword;
    }
    

    /**
     *  Set apiParameters
     *  @param apiParameters
     */
    public void setApiParameters(String apiParameters){
        this.apiParameters = apiParameters;
    }

    /**
     *  Get for apiParameters
     *  @return String
     */
    public String getApiParameters(){
        return this.apiParameters;
    }
    

    /**
     *  Set visualizationURL
     *  @param visualizationURL
     */
    public void setVisualizationURL(String visualizationURL){
        this.visualizationURL = visualizationURL;
    }

    /**
     *  Get for visualizationURL
     *  @return String
     */
    public String getVisualizationURL(){
        return this.visualizationURL;
    }
    

    /**
     *  Set exploreButtonURL
     *  @param exploreButtonURL
     */
    public void setExploreButtonURL(String exploreButtonURL){
        this.exploreButtonURL = exploreButtonURL;
    }

    /**
     *  Get for exploreButtonURL
     *  @return String
     */
    public String getExploreButtonURL(){
        return this.exploreButtonURL;
    }
    

    /**
     *  Set exploreButtonOpensNewWindow
     *  @param exploreButtonOpensNewWindow
     */
    public void setExploreButtonOpensNewWindow(boolean exploreButtonOpensNewWindow){
        this.exploreButtonOpensNewWindow = exploreButtonOpensNewWindow;
    }

    /**
     *  Get for exploreButtonOpensNewWindow
     *  @return boolean
     */
    public boolean getExploreButtonOpensNewWindow(){
        return this.exploreButtonOpensNewWindow;
    }
    

    /**
     *  Set contactName
     *  @param contactName
     */
    public void setContactName(String contactName){
        this.contactName = contactName;
    }

    /**
     *  Get for contactName
     *  @return String
     */
    public String getContactName(){
        return this.contactName;
    }
    

    /**
     *  Set contactEmail
     *  @param contactEmail
     */
    public void setContactEmail(String contactEmail){
        this.contactEmail = contactEmail;
    }

    /**
     *  Get for contactEmail
     *  @return String
     */
    public String getContactEmail(){
        return this.contactEmail;
    }
    

    /**
     *  Set serviceActive
     *  @param serviceActive
     */
    public void setServiceActive(boolean serviceActive){
        this.serviceActive = serviceActive;
    }

    /**
     *  Get for serviceActive
     *  @return boolean
     */
    public boolean getServiceActive(){
        return this.serviceActive;
    }
    

    /**
     *  Set serviceInactiveMessage
     *  @param serviceInactiveMessage
     */
    public void setServiceInactiveMessage(String serviceInactiveMessage){
        this.serviceInactiveMessage = serviceInactiveMessage;
    }

    /**
     *  Get for serviceInactiveMessage
     *  @return String
     */
    public String getServiceInactiveMessage(){
        return this.serviceInactiveMessage;
    }
    

    /**
     *  Set serviceDownMessage
     *  @param serviceDownMessage
     */
    public void setServiceDownMessage(String serviceDownMessage){
        this.serviceDownMessage = serviceDownMessage;
    }

    /**
     *  Get for serviceDownMessage
     *  @return String
     */
    public String getServiceDownMessage(){
        return this.serviceDownMessage;
    }
    

    /**
     *  Set updated
     *  @param updated
     */
    public void setUpdated(Timestamp updated){
        this.updated = updated;
    }

    /**
     *  Get for updated
     *  @return Timestamp
     */
    public Timestamp getUpdated(){
        return this.updated;
    }
    

    /**
     *  Set created
     *  @param created
     */
    public void setCreated(Timestamp created){
        this.created = created;
    }

    /**
     *  Get for created
     *  @return Timestamp
     */
    public Timestamp getCreated(){
        return this.created;
    }
    
public String asJSON(){

    // Initialize JSON response
    JsonObjectBuilder jsonData = Json.createObjectBuilder();

    	jsonData.add("id", this.id == null ? -99 : this.id)
	        .add("serviceName", this.serviceName == null ? JsonValue.NULL : this.serviceName)
	        .add("serviceDescription", this.serviceDescription == null ? JsonValue.NULL : this.serviceDescription)
	        .add("apiEndpointURL", this.apiEndpointURL == null ? JsonValue.NULL : this.apiEndpointURL)
	        .add("apiUsername", this.apiUsername == null ? JsonValue.NULL : this.apiUsername)
	        .add("apiEncryptedPassword", this.apiEncryptedPassword == null ? JsonValue.NULL : this.apiEncryptedPassword)
	        .add("apiParameters", this.apiParameters == null ? JsonValue.NULL : this.apiParameters)
	        .add("visualizationURL", this.visualizationURL == null ? JsonValue.NULL : this.visualizationURL)
	        .add("exploreButtonURL", this.exploreButtonURL == null ? JsonValue.NULL : this.exploreButtonURL)
	        .add("exploreButtonOpensNewWindow", this.exploreButtonOpensNewWindow)
	        .add("contactName", this.contactName == null ? JsonValue.NULL : this.contactName)
	        .add("contactEmail", this.contactEmail == null ? JsonValue.NULL : this.contactEmail)
	        .add("serviceActive", this.serviceActive)
	        .add("serviceInactiveMessage", this.serviceInactiveMessage == null ? JsonValue.NULL : this.serviceInactiveMessage)
	        .add("serviceDownMessage", this.serviceDownMessage == null ? JsonValue.NULL : this.serviceDownMessage)
	        .add("updated", this.updated == null ? JsonValue.NULL : this.updated)
	        .add("created", this.created == null ? JsonValue.NULL : this.created);

    return jsonData.build().toString();

    }
