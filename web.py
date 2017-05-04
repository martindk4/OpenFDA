import http.server
import socketserver
import json
import http.client


class OpenFDAClient():
    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"
    OPENFDA_API_SEARCH="?limit=10&search=patient.drug.medicinalproduct:"
    OPENFDA_API_SEARCH_COMPANY="?limit=10&search=companynumb:"

    def get_events(self,limite):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit='+str(limite))
        resp = conn.getresponse()
        resp_read = resp.read()
        respf= resp_read.decode("utf8")
        events= respf
        return events

    def get_event_search(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_SEARCH+ drug)
        resp = conn.getresponse()
        resp_read = resp.read()
        respf= resp_read.decode("utf8")
        events_search= respf
        return events_search

    def get_event_search_2(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_SEARCH_COMPANY+company)
        resp = conn.getresponse()
        resp_read = resp.read()
        respf= resp_read.decode("utf8")
        events_search_2= respf
        return events_search_2

class OpenFDAParser():
    def get_drugs_from_events(self,events):
        drugs=[]
        for event in events:
            drugs+=[event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_genders_from_events(self,events):
        genders=[]
        for event in events:
            genders+=[event['patient']['patientsex']]
        return genders

    def get_companies_from_events(self,events_search):
        companies=[]
        for event in events_search:
            companies+=[event["companynumb"]]
        return companies

class OpenFDAHTML():

    def get_main_page(self):
        html="""
        <html>
            <head>
            </head>
            <body>
                <h1></h1>
                <form method="get"action="listDrugs">
                    <input type= "submit" value ="Drug List: Enviar">
                    LIMITE:<input type= "text" name ="limite">
                    </input>
                </form>
                <form method="get" action = "searchDrug">
                    <input type= "submit" value ="Drug Search: Sent to OpenFDA">
                    <input type= "text" name ="drug">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type= "submit" value ="Companynumb List: Enviar"></input>
                    LIMITE:<input type= "text" name ="limite">
                    </input>
                </form>
                <form method="get" action = "searchCompany">
                    <input type= "submit" value ="Companynumb Search: Sent to OpenFDA">
                    <input type= "text" name ="company">
                    </input>
                </form>
                <form method="get" action="listGender">
                    <input type= "submit" value ="Gender List: Enviar">
                    LIMITE:<input type= "text" name ="limite">
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def get_third_page(self):
        html="""
        <html>
            <head>
            </head>
            <body>
            Error: Resource does not exist
            </body>
        </html>
        """
        return html

    def get_second_page(self,drugs):

        list_drugs= """
        <html>
            <head>
                <tittle></tittle>
            </head>
            <body>
                <ol>
        """

        for drug in drugs:
            list_drugs +="<li>"+drug+ "</li>"
        list_drugs += """

                </ol>
            </body>
        </html>
        """
        return list_drugs

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        html_1=OpenFDAHTML()
        parser=OpenFDAParser()
        client=OpenFDAClient()

        main_page = False
        is_event = False
        is_search = False
        is_companynumb = False
        is_companysearch = False
        is_gender = False
        no_found = False

        if self.path =="/":
            main_page = True

        elif "/listDrugs" in self.path:
            is_event = True

        elif "searchDrug" in self.path:
            is_search = True

        elif "/listCompanies" in self.path:
            is_companynumb = True

        elif "searchCompany" in self.path:
            is_companysearch = True

        elif "listGender" in self.path:
            is_gender = True

        else:
            no_found = True
            self.send_response(404)

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        html = html_1.get_main_page()

        if main_page:
            self.wfile.write(bytes(html, "utf8"))
        elif is_event:
            limite=str(self.path.split('=')[1])
            events_str= client.get_events(limite)
            events=json.loads(events_str)
            events=events['results']
            drugs= parser.get_drugs_from_events(events)
            self.wfile.write(bytes(html_1.get_second_page(drugs), "utf8"))

        elif is_search:
            drug= self.path.split('=')[1]
            events_search=client.get_event_search(drug)
            events_search=json.loads(events_search)
            events1=events_search['results']
            companies=parser.get_companies_from_events(events1)
            html2=html_1.get_second_page(companies)
            self.wfile.write(bytes(html2,"utf8"))

        elif is_companynumb:
            limite=str(self.path.split('=')[1])
            events_str= client.get_events(limite)
            events=json.loads(events_str)
            events=events['results']
            companynumbs= parser.get_companies_from_events(events)
            self.wfile.write(bytes(html_1.get_second_page(companynumbs), "utf8"))

        elif is_companysearch:
            company=self.path.split('=')[1]
            event_search_2=client.get_event_search_2(company)
            events_search_2=json.loads(event_search_2)
            events2=events_search_2['results']
            companydrugs=parser.get_drugs_from_events(events2)
            html2=html_1.get_second_page(companydrugs)
            self.wfile.write(bytes(html2,"utf8"))

        elif is_gender:
            limite=str(self.path.split('=')[1])
            events_str= client.get_events(limite)
            events=json.loads(events_str)
            events=events['results']
            genders= parser.get_genders_from_events(events)
            self.wfile.write(bytes(html_1.get_second_page(genders), "utf8"))

        else:
            self.wfile.write(bytes(html_1.get_third_page(), "utf8"))

        return
