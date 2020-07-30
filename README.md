# python-qr-code-generator-api
A simple Python wrapper for the API of qr-code-generator.com, which is used to generate QR codes with certain design elements.

## Why this API wrapper?
First of all, because I needed it and also because this API is not really [well documented](https://www.qr-code-generator.com/qr-code-api/). This wrapper provides a quick and easy way to connect to the API and request images, with a minimal amount of coding or effort. Just import the module, write a couple lines of easily understandable code and start generating these amazing QR codes.

## Features
### Configure to fit your own needs
While we have the wrapper set up in a way that allows for quick usage of the API, we understand that sometimes you just need it to test an absurd scenario or that you want to change output folders. With the configuration file, you are the boss. Even better: you don't necessarily have to change the configuration file to work for you. If you want, you can just use code to update configuration variables and run a request. This way, your configuration is limited to your own code.

### Change all possible QR code options
This wrapper provides an easy way to update QR options. Just set the dictionary variable to a new value, and it will automatically be taken into account when generating a code.

### Automatically save QR codes
The wrapper takes the API response and automatically turns it into a saved image in the desired output location. Do we need to say more?

## Usage
The wrapper was developed with ease of use in mind. This means that one can either, directly call the module to perform a request, or code their own Python scripts and import the module.

### Command Line Interface
To perform a request via the command line, simply ```$ python3 qr_code_generator``` with flags to specify your needs. The following flags are supported: 
* --token <token> (short: -t)
* --load <path to yaml settings file> (short: -l)
* --output <the output file name> (short: -o)
* --bulk <amount of codes to generate> (short: -b)
* --verbose (short -v)

## Authentication
There are three possible ways to authenticate with the API. Authentication is done on a token basis. A token can be generated [on this webpage](https://app.qr-code-generator.com/api/). The three ways are (based from most safe to least safe, and thus least preferred):

### Environment variables
The safest way to authenticate, is by using environment variables. This starts by exporting your access key to an environment variable with ```$ export ACCESS_TOKEN=<your token here>```. After this, feel free to create an instance of QrGenerator by just calling the class as ```api = QrGenerator()```. The token will automatically be fetched from the environment.

### Hardcoded in your own code
A little bit less safe, because what if you accidentally commit your code with the token in it, or what if someone finds a readable portion of your code? If you choose to go down this route, understand that there are certain risks involved, but it can be done. There are two ways to put the token in your own code.
1. Either make sure you call the QrGenerator class with a token parameter, as such: ```api = QrGenerator(<your token here>)```. This will fetch the token from your code and add it to the query.
2. Or set it later in your code, by using the set function: ```QrGenerator.set('access-token', <your token here>)```.

When ```QrGenerator.request()``` is called and the API token has not been set and the configuration file has not been altered, a custom Exception will be thrown: ```MissingRequiredParameterError```. This is because the API will directly return an InvalidCredentialsError regardless. If the configuration file has been changed, you might encounter a ```InvalidCredentialsError```. Either way, it will not work.
