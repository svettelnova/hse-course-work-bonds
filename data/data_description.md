find da data in [here](https://drive.google.com/drive/folders/1IG5fi5MY1qWTK6NgCGDDzUAhwzyxDk1W?usp=share_link) 

### bond_data_ai.csv

columns:
- isin -- international Securities Identification Numbering system
- date -- trade date
- ai -- accrued interest 

### bond_data_coupon.csv

columns:
- isin -- international Securities Identification Numbering system
- period_from_calc -- Дата начала действия ставки/правила
- period_to_calc -- Дата окончания действия ставки/правила
- payment_date_calc -- Дата реальной выплаты купона 
- coupon_rate -- Ставка купона, процентов годовых

### bond_data_duration.csv
Precomputed duration data

columns:
- id -- cbonds id
- date -- trade date 
- isin -- international Securities Identification Numbering system
- emission_id -- cbonds emission id
- emission_emitent_id -- cbonds issuer id
- trading_ground_id -- trading ground 
- avar_price -- average price 
- convexity -- 
- convexity_offer
- dur -- bond duration 
- dur_to -- use if `dur` is null or 0
- dur_mod -- modified duration 
- dur_mod_to -- use if `dur_mod` is null or 0

### bond_data_filled_price.csv

columns:
- same as in bond_data_price.csv

### bond_data_notionals.csv

columns:
- isin -- international Securities Identification Numbering system
- mty_part -- list of values: amount of face value paid   
- mty_date -- list of dates: date on which corresponding face value is being paid  

### bond_data_price.csv
Bonds historical prices 

columns:
- isin -- international Securities Identification Numbering system
- date -- trade date
- spread -- ask - bid
- ask  
- bid  
- ai -- accrued interest
- last -- latest price
- mid -- (bid + ask) / 2

### bond_data_rating.csv
Bond ratings data

columns:
- update_date 
- fintoolid -- tool id 
- rating -- rating description 
- rating_cleaned -- rating value
- num_rating -- custom numerical representation of rating 
- isincode -- international Securities Identification Numbering system

### bond_data_rgbitr.csv

columns:
- date -- trade date
- secid -- security id 
- yield 
- duration 
- close -- close price 


### bond_data_spreads.csv

columns:
- isin -- international Securities Identification Numbering system
- date -- trade date

### bond_data_static.csv
Static bond info including coupon data

columns:
- https://docs.efir-net.ru/dh2/#/Info/FintoolReferenceData

### bond_data_volume.csv
Traded volume data

columns:
- isin -- international Securities Identification Numbering system
- date -- trade date
- volume -- traded volume 
- volume_lots -- number of traded lots

### bond_data_yield.csv
Estimated bond yields

columns:
- isin -- international Securities Identification Numbering system
- date -- trade date 
- yield 
