*** Variables ***

${search-input}   xpath=//input[contains(@class, 'search-input')]
${search-location-result}   xpath=//div[@class="results-container"]//p[@class="search-bar-result__name" and text()="<<param>>"]
${accept-privacy-button}   id=ketch-banner-button-primary
${menu-items}   xpath=//a[@data-gaid="<<param>>"]
${daily-weather-card}   xpath=//a[contains(@class, "daily-forecast-card")]
${threedot-menu}   xpath=//*[name()='svg' and contains(@class, 'hamburger-button')]
${settings}   xpath=//*[name()='svg' and contains(@class, 'icon-settings')]//parent::a
${unit-setting}   xpath=//select[@id="unit"]
${logo-icon}    xpath=//a[@class="header-logo"]

#card loading
${content-module}   div.content-module

#daily page
${content-modules}   xpath=//a[@class="daily-forecast-card "]
${content-cards}   xpath=//div[contains(@class, "half-day-card${SPACE}  content-module")]
${day-label}   xpath=//div[@class="subnav-pagination"]/div
${temperature-label}   ${content-cards}//div[@class="temperature"]
${real-feel-label}   xpath=//div[@class="real-feel"]
${main-weather-label}   xpath=//div[@class="half-day-card-content"]/div[@class="phrase"]
${humidity-label}   xpath=//p[text()="Humidity"]/span
${quarter-day-weather-link}   xpath=//a[contains(@href, "<<param>>-weather-forecast")]
${morning-button}   xpath=//a[contains(text(), "Morning")]
${afternoon-button}   xpath=//a[contains(text(), "Afternoon")]

#today page
${current-temperature}   xpath=//div[contains(@class, "temp-container")]
${current-weather}   xpath=//div[@class="cur-con-weather-card__panel"]//span[@class="phrase"]
${current-time}   xpath=//div[@class="title-container"]//p
