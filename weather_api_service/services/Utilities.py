from weather_api_service import db
import json
from pathlib import Path
from collections import Counter
from weather_api_service.models.Analytics import Audit
from flask import request


class Utilities:

    def ReadCountryFile() -> dict:
        countryDict = {}
        mod_path = Path(__file__).parent
        rel_path = '../data/country_data.json'
        path =  (mod_path / rel_path).resolve()
        
        with open(path, 'r', encoding='utf-8') as f:
            cont = f.read()
        data = json.loads(cont)
        
        for elem in data:
            try:
                countryDict[elem['country']].append(elem['name'])
            except:
                countryDict[elem['country']] = [elem['name']]

        return countryDict

    
    def FindTopN(find_type, payload):
        data, status, message = None, None, None   
        try:        
            rows = Audit.query.all()
            n: int = int(payload['n'])
            top_n = {}
            if rows and n:
                if find_type == 'Countries':
                    user_list = [row.country for row in rows if len(row.country) > 0]
                elif find_type == 'Cities':
                    user_list = [row.city for row in rows if len(row.city) > 0]
                else:
                    user_list = [row.username for row in rows if len(row.username) > 0]

                top = Counter(user_list).most_common(n)
                for elem, freq in top:
                    top_n[elem] = freq   
                    
                data, status, message = top_n, 200, f'Successfully Listed Top {n} {find_type}'
            else:
                status, message = 500, f'Failed to List Top {n} {find_type}'
            
        except Exception as e:
            message, status = f'Exception has occured - {str(e)}', 500

        return data, status, message


    def CommitAnalyticsDB(date, country, city, cur_user, message):
        audit = Audit(date, country, city, cur_user, message)
        db.session.add(audit)
        db.session.commit()