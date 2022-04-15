# Vehicle-detection


## Vehicle detector
We Splitted the given document into sentences and retrieved source, destination, and vehicle names from each one.
### Example
```
from vehicle_detector import VehicleDetector
vehicle_detector = VehicleDetector()
vehicle_detector.run('.من با قطار از تهران به اصفهان می روم')
```

### Output

```
[
  {
    'from': 'تهران',
    'from_span': [14, 19],
    'to': 'اصفهان',
    'to_span': [23, 29],
    'vehicle': 'قطار',
    'vehicle_span': [6, 10]
  }
]
```

## Contributors
Roya ghavami\
Ali rezaei\
Mohammadali Hosseinnezhad
