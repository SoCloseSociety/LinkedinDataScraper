from bs4 import BeautifulSoup

html = """ <div class="ph0 pv2 artdeco-card mb2">
<!---->        <ul class="reusable-search__entity-result-list list-style-none">
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:768950576">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/in/fatih-birol?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC3VQTABcwTK61w9OFN_magDx3L8HlSM04A">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
<!---->        
<div class="presence-entity presence-entity--size-3">
  <img src="https://media-exp1.licdn.com/dms/image/C4D03AQHeAG-UaE0YAQ/profile-displayphoto-shrink_100_100/0/1632471358742?e=1667433600&amp;v=beta&amp;t=Zj7OYRIJNnjqBfdsZgMwWc7vfYNdfJ0zp_uN65Y4-NY" loading="lazy" alt="Fatih Birol" id="ember100" class="presence-entity__image  ivm-view-attr__img--centered EntityPhoto-circle-3  EntityPhoto-circle-3 lazy-image ember-view">

  
<div class="presence-entity__indicator
      
      presence-entity__indicator--size-3 presence-indicator
    hidden
    presence-indicator--size-3">
  <span class="visually-hidden">
      Status is offline
      </span>
</div>
</div>

</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/in/fatih-birol?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC3VQTABcwTK61w9OFN_magDx3L8HlSM04A">
        <span dir="ltr"><span aria-hidden="true"><!---->Fatih Birol<!----></span><span class="visually-hidden"><!---->View Fatih Birol’s profile<!----></span></span>
      </a>
        <span class="entity-result__badge t-14 t-normal t-black--light">
          <div class="display-flex
    flex-row-reverse
    align-items-baseline">
    <div class="ivm-image-view-model    flex-shrink-zero align-self-center mr2 entity-result__badge-icon ml1">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <li-icon type="linkedin-bug-influencer-color" size="small" role="img" aria-label="Influencer"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" data-supported-dps="16x16" class="mercado-match" width="16" height="16" focusable="false">
  <path d="M14 0H2a1 1 0 00-1 1v15l3-2h10a1 1 0 001-1V1a1 1 0 00-1-1zM5 12H3V5h2zM4 4.2A1.27 1.27 0 012.75 3a1.25 1.25 0 012.5 0A1.27 1.27 0 014 4.2zm9 7.8h-2V8.73c0-.79-.18-1.93-1.34-1.93A1.74 1.74 0 008 8.61V12H6V5h1.85v1a2.72 2.72 0 012.29-1.2C12.27 4.8 13 6.09 13 8.29z" fill="#0a66c2"></path>
</svg></li-icon>
</div>
  </div>
    <span class="image-text-lockup__text entity-result__badge-text">
      <span aria-hidden="true"><!---->• 3rd+<!----></span><span class="visually-hidden"><!---->3rd+ degree connection<!----></span>
    </span>
</div>
        </span>
    </span>
  </span>
    <span aria-hidden="true" class="entity-result__badge-overflow align-self-flex-end t-14 t-normal t-black--light flex-shrink-zero
        ">
      <div class="display-flex
    flex-row-reverse
    align-items-baseline">
    <div class="ivm-image-view-model    flex-shrink-zero align-self-center mr2 entity-result__badge-icon ml1">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <li-icon type="linkedin-bug-influencer-color" size="small" role="img" aria-label="Influencer"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" data-supported-dps="16x16" class="mercado-match" width="16" height="16" focusable="false">
  <path d="M14 0H2a1 1 0 00-1 1v15l3-2h10a1 1 0 001-1V1a1 1 0 00-1-1zM5 12H3V5h2zM4 4.2A1.27 1.27 0 012.75 3a1.25 1.25 0 012.5 0A1.27 1.27 0 014 4.2zm9 7.8h-2V8.73c0-.79-.18-1.93-1.34-1.93A1.74 1.74 0 008 8.61V12H6V5h1.85v1a2.72 2.72 0 012.29-1.2C12.27 4.8 13 6.09 13 8.29z" fill="#0a66c2"></path>
</svg></li-icon>
</div>
  </div>
    <span class="image-text-lockup__text entity-result__badge-text">
      <span aria-hidden="true"><!---->• 3rd+<!----></span><span class="visually-hidden"><!---->3rd+ degree connection<!----></span>
    </span>
</div>
    </span>
</div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Executive Director at International Energy Agency (IEA)<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            mb1">
          <!---->Summary: Executive<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>of IEA, the global authority on<span class="white-space-pre"> </span><strong><!---->energy<!----></strong><!---->. Big Galatasaray fan.<!---->
        </p>
      
</div>

      <div class="entity-result__insights t-12">
        
              
                  <div class="entity-result__simple-insight ">
    
        <div class="ivm-image-view-model    entity-result__simple-insight-image flex-shrink-zero mr2">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <li-icon aria-hidden="true" type="people" size="small"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" data-supported-dps="16x16" fill="currentColor" class="mercado-match" width="16" height="16" focusable="false">
  <path d="M14 11.75V15H9v-3.25A1.75 1.75 0 0110.75 10h1.5A1.75 1.75 0 0114 11.75zM11.5 9A2.5 2.5 0 109 6.5 2.5 2.5 0 0011.5 9zM5 1a3 3 0 103 3 3 3 0 00-3-3zm.75 7h-1.5A2.25 2.25 0 002 10.25V15h6v-4.75A2.25 2.25 0 005.75 8z"></path>
</svg></li-icon>
</div>
  </div>
      <div class="entity-result__simple-insight-text-container">
        <span class="entity-result__simple-insight-text
            entity-result__simple-insight-text--small">
          <!---->69.3K followers<!---->
        </span>
<!---->      </div>
    
</div>

<!---->
<!---->
            
          
      </div>
  </div>
  <div class="entity-result__actions entity-result__divider">
<!---->      
              
  <div>
<!---->          <button data-test-reusable-search-primary-action="true" data-control-id="y5K85piFSkiIR4FNeA2rLw==" data-control-name="entity_action_primary" aria-label="Follow" id="ember109" class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"><!---->
<span class="artdeco-button__text">
    Follow
</span></button>
</div>

          
  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <div class="EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ">
<!---->    </div>
</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director chez Suez Energy<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current:<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>at Suez<span class="white-space-pre"> </span><strong><!---->Energy<!----></strong>
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <div class="EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ">
<!---->    </div>
</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div>
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director at Dominion Energy<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

<!---->
<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <div class="EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ">
<!---->    </div>
</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Managing Director &amp; Senior Partner chez Boston Consulting Group | Energy &amp; Utilities<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current: Managing<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>&amp; Senior Partner at Boston Consulting Group (BCG)<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
<!---->        
<div class="presence-entity presence-entity--size-3">
  <img src="https://media-exp1.licdn.com/dms/image/C5603AQFL7_I4Dx6j7A/profile-displayphoto-shrink_100_100/0/1609787892792?e=1667433600&amp;v=beta&amp;t=2dGdad2bRJVme5HrmscKstAu11v6srYiM92LyJ7HKH8" loading="lazy" id="ember101" class="presence-entity__image  ivm-view-attr__img--centered EntityPhoto-circle-3  EntityPhoto-circle-3 lazy-image ember-view" role="presentation">

  
<div class="presence-entity__indicator
      
      presence-entity__indicator--size-3 presence-indicator
    hidden
    presence-indicator--size-3">
  <span class="visually-hidden">
      Status is offline
      </span>
</div>
</div>

</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director - EDF Local Energy Management<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Paris<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current: Directeur / EDF - Local<span class="white-space-pre"> </span><strong><!---->Energy<!----></strong><span class="white-space-pre"> </span>Management at EDF<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:1080443">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/in/philippedav?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAQfHsBoWhC3fEI22EoROx2sdZzhzWYpvo">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
<!---->        
<div class="presence-entity presence-entity--size-3">
  <img src="https://media-exp1.licdn.com/dms/image/C4D03AQHUjqL7se1tww/profile-displayphoto-shrink_100_100/0/1571236456325?e=1667433600&amp;v=beta&amp;t=PRYKV7ql3VN418AtLbOsC-lxEOiUh8KPBHf3633_jaA" loading="lazy" alt="Philippe DAVID" id="ember102" class="presence-entity__image  ivm-view-attr__img--centered EntityPhoto-circle-3  EntityPhoto-circle-3 lazy-image ember-view">

  
<div class="presence-entity__indicator
      
      presence-entity__indicator--size-3 presence-indicator
    hidden
    presence-indicator--size-3">
  <span class="visually-hidden">
      Status is offline
      </span>
</div>
</div>

</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/in/philippedav?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAQfHsBoWhC3fEI22EoROx2sdZzhzWYpvo">
        <span dir="ltr"><span aria-hidden="true"><!---->Philippe DAVID<!----></span><span class="visually-hidden"><!---->View Philippe DAVID’s profile<!----></span></span>
      </a>
        <span class="entity-result__badge t-14 t-normal t-black--light">
          <div class="display-flex
    flex-row-reverse
    align-items-baseline">
    <div class="ivm-image-view-model    flex-shrink-zero align-self-center mr2 entity-result__badge-icon ml1">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <li-icon type="linkedin-bug" size="14dp" color="premium" role="img" aria-label="Premium member"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 14" data-supported-dps="14x14" fill="currentColor" class="mercado-match" width="14" height="14" focusable="false">
  <g>
    <path class="background-mercado" d="M14 1v12a1 1 0 01-1 1H1a1 1 0 01-1-1V1a1 1 0 011-1h12a1 1 0 011 1zM4 5H2v7h2zm.25-2A1.27 1.27 0 003 1.8 1.27 1.27 0 001.75 3 1.27 1.27 0 003 4.2 1.27 1.27 0 004.25 3zM12 8.29c0-2.2-.73-3.49-2.86-3.49A2.71 2.71 0 006.89 6V5H5v7h2V8.73A1.74 1.74 0 018.66 6.8C9.82 6.8 10 7.94 10 8.73V12h2z"></path>
  </g>
</svg></li-icon>
</div>
  </div>
    <span class="image-text-lockup__text entity-result__badge-text">
      <span aria-hidden="true"><!---->• 3rd+<!----></span><span class="visually-hidden"><!---->3rd+ degree connection<!----></span>
    </span>
</div>
        </span>
    </span>
  </span>
    <span aria-hidden="true" class="entity-result__badge-overflow align-self-flex-end t-14 t-normal t-black--light flex-shrink-zero
        ">
      <div class="display-flex
    flex-row-reverse
    align-items-baseline">
    <div class="ivm-image-view-model    flex-shrink-zero align-self-center mr2 entity-result__badge-icon ml1">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <li-icon type="linkedin-bug" size="14dp" color="premium" role="img" aria-label="Premium member"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 14" data-supported-dps="14x14" fill="currentColor" class="mercado-match" width="14" height="14" focusable="false">
  <g>
    <path class="background-mercado" d="M14 1v12a1 1 0 01-1 1H1a1 1 0 01-1-1V1a1 1 0 011-1h12a1 1 0 011 1zM4 5H2v7h2zm.25-2A1.27 1.27 0 003 1.8 1.27 1.27 0 001.75 3 1.27 1.27 0 003 4.2 1.27 1.27 0 004.25 3zM12 8.29c0-2.2-.73-3.49-2.86-3.49A2.71 2.71 0 006.89 6V5H5v7h2V8.73A1.74 1.74 0 018.66 6.8C9.82 6.8 10 7.94 10 8.73V12h2z"></path>
  </g>
</svg></li-icon>
</div>
  </div>
    <span class="image-text-lockup__text entity-result__badge-text">
      <span aria-hidden="true"><!---->• 3rd+<!----></span><span class="visually-hidden"><!---->3rd+ degree connection<!----></span>
    </span>
</div>
    </span>
</div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Managing Director &amp; Partner at Boston Consulting Group | Technology Advantage, Energy &amp; Utilities, Construction, Industrial Goods, Transportation &amp; Logistics<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Paris<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current: Managing<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>&amp; Partner at Boston Consulting Group (BCG)<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider">
<!---->      
              
  <div>
              <button aria-label="Invite Philippe DAVID to connect" id="ember110" class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"><!---->
<span class="artdeco-button__text">
    Connect
</span></button>

<!---->
<!---->

</div>

          
  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <div class="EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ">
<!---->    </div>
</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Managing Director chez Pierce Energy Planning<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current: Managing<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>at Pierce<span class="white-space-pre"> </span><strong><!---->Energy<!----></strong><span class="white-space-pre"> </span>Planning<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
<!---->        
<div class="presence-entity presence-entity--size-3">
  <img src="https://media-exp1.licdn.com/dms/image/C4D03AQF4bQJxMWjObw/profile-displayphoto-shrink_100_100/0/1592224553272?e=1667433600&amp;v=beta&amp;t=RuSzuItaL3bjdPs6oB6-FTSwbfMB_8DG1Yi8K7D5UDQ" loading="lazy" id="ember103" class="presence-entity__image  ivm-view-attr__img--centered EntityPhoto-circle-3  EntityPhoto-circle-3 lazy-image ember-view" role="presentation">

  
<div class="presence-entity__indicator
      
      presence-entity__indicator--size-3 presence-indicator
    hidden
    presence-indicator--size-3">
  <span class="visually-hidden">
      Status is offline
      </span>
</div>
</div>

</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director - Oil, Gas and Energy Industry Business Unit<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->France<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current:<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>- Oil &amp; Gas Industry Business Unit at SAP<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
    <div class="EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ">
<!---->    </div>
</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director - Abyss Energy<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->Greater Paris Metropolitan Region<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current:<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>at Abyss<span class="white-space-pre"> </span><strong><!---->Energy<!----></strong>
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
          <li class="reusable-search__result-container ">
            
          
              
          <div class="entity-result" data-chameleon-result-urn="urn:li:member:headless">
        
        <div class="entity-result__item">
  <div class="entity-result__universal-image">
    <div class="display-flex align-items-center">
<!---->        
            <a class="app-aware-link scale-down " aria-hidden="true" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
    <div class="ivm-image-view-model   ">
    <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
    
    ">
<!---->        
<div class="presence-entity presence-entity--size-3">
  <img src="https://media-exp1.licdn.com/dms/image/C4D03AQHKY93KwERybw/profile-displayphoto-shrink_100_100/0/1556740261433?e=1667433600&amp;v=beta&amp;t=TFkCSMDdSYf4FV7FxfDhcEqqgRZgTNIe4j-YWVxb4xA" loading="lazy" id="ember104" class="presence-entity__image  ivm-view-attr__img--centered EntityPhoto-circle-3  EntityPhoto-circle-3 lazy-image ember-view" role="presentation">

  
<div class="presence-entity__indicator
      
      presence-entity__indicator--size-3 presence-indicator
    hidden
    presence-indicator--size-3">
  <span class="visually-hidden">
      Status is offline
      </span>
</div>
</div>

</div>
  </div>
</a>
          
    </div>
  </div>
  <div class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light">
    <div class="mb1">
      
<div class="t-roman t-sans">
  
            
            <div class="display-flex">
  <span class="entity-result__title-line entity-result__title-line--2-lines">
    <span class="entity-result__title-text t-16">
      <a class="app-aware-link" href="https://www.linkedin.com/search/results/people/headless?geoUrn=%5B106383538%5D&amp;origin=FACETED_SEARCH&amp;keywords=director%20in%20energy">
        <!---->LinkedIn Member<!---->
      </a>
<!---->    </span>
  </span>
<!----></div>
          
        
</div>

    <div class="linked-area flex-1
    cursor-pointer">
  
      
    <div>
      <div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!---->Director - M&amp;A Energy &amp; Renewables<!---->
      </div>
        <div class="entity-result__secondary-subtitle t-14 t-normal">
          <!---->France<!---->
        </div>
    </div>

  

    
</div>

    </div>

      <div class="linked-area flex-1
    cursor-pointer">
  
        <p class="entity-result__summary
            entity-result__summary--2-lines
            t-12 t-black--light
            ">
          <!---->Current:<span class="white-space-pre"> </span><strong><!---->Director<!----></strong><span class="white-space-pre"> </span>- M&amp;A<span class="white-space-pre"> </span><strong><!---->Energy<!----></strong><span class="white-space-pre"> </span>&amp; Renewables at BNP Paribas CIB<!---->
        </p>
      
</div>

<!---->  </div>
  <div class="entity-result__actions entity-result__divider entity-result__actions--empty">
<!----><!---->  </div>
</div>
      

</div>
      
            
<!---->        
          </li>
</ul>
    
<!---->
    
              
<!---->      
            
  </div>                           """

soup = BeautifulSoup(html, "html.parser")

for search_rslt_tag in soup.find_all("div", {"class": "ph0 pv2 artdeco-card mb2"}):
    for a in search_rslt_tag.find_all('a', href=True):
        print (a['href'])

    for designation in search_rslt_tag.find_all('div', {"class":"entity-result__primary-subtitle t-14 t-black t-normal"}):
        print (designation.text)
    

       
