config = {
	"sql_credentials": "mysql://user:pass@localhost",
	"sql_db_name": "curtain",
    
    "gpio_pins": [1,2,3,4,5,6],
	"pinout": {
		"top_roller": {
			"power": 6,
			"up": 5,
			"down" 4
		},
		"bottom_roller": {
			"power": 3,
			"up": 2,
			"down" 1
		},
	},
}