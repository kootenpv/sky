DEFAULT_CRAWL_CONFIG = {
    # Required
    'seed_urls' : [
    
    ],
    
    'collections_path' : '',

    'collection_name' : '',

    # Optional
    
    'crawl_filter_strings' : [
                        
    ],

    'crawl_required_strings' : [
    ],        
            
    'index_filter_strings' : [
        
    ],
    
    'index_required_strings' : [
                          
    ], 

    'exclude' : None, 
    'strict' : True, 
    'max_redirects_per_url' : 10, 
    'max_tries_per_url' : 1, 
    'max_workers' : 100,
    
    'wait_between_url_visits_in_seconds' : 1,
    
    'max_saved_responses' : 100,
    
    'usernameField' : '',
    'usernameValue' : '',
    'passwordField' : '', 
    'passwordValue' : '',
 
    'max_hops' : 100,
    'browser': 'U'
}

