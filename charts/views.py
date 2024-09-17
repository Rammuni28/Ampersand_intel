import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StCompanyOverview, StFundingValuation,StOwnershipStructure,StParametricScoring
from django.forms.models import model_to_dict
from .session import Session  # Import the scoped session
from django.http import JsonResponse

def sqlalchemy_obj_to_dict(obj):
    """Convert a SQLAlchemy object into a dictionary."""
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
# Company Overview List View (GET, POST)
class StCompanyOverviewList(APIView):
    
    # GET - Retrieve all companies
    def get(self, request, *args, **kwargs):
        session = Session()  # Create a new session instance
        try:
            companies = session.query(StCompanyOverview).all()
            companies_data = [sqlalchemy_obj_to_dict(company) for company in companies]
            return Response(companies_data, status=status.HTTP_200_OK)
        finally:
            Session.remove()  # Properly clean up the session after the request

    # POST - Create a new company overview entry
    def post(self, request, *args, **kwargs):
        session = Session()
        try:
            data = request.data
            new_company = StCompanyOverview(
                st_company_name=data['st_company_name'],
                st_company_description=data['st_company_description'],
                st_year_of_incorporation=data['st_year_of_incorporation'],
                st_country=data['st_country'],
                st_total_founders=data['st_total_founders'],
                st_no_of_employees=data['st_no_of_employees'],
                st_founder_names=data['st_founder_names'],
                st_industry_type=data['st_industry_type'],
                st_geography=data['st_geography'],
                is_active=data.get('is_active', True)
            )
            session.add(new_company)
            session.commit()
            return Response({'message': 'Company created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()  # Clean up the session

# Company Overview Detail View (GET, PUT, DELETE)
class StCompanyOverviewDetail(APIView):
    
    # Helper method to get a specific company overview by ID
    def get_object(self, st_company_id, session):
        try:
            return session.query(StCompanyOverview).filter(StCompanyOverview.st_company_id == st_company_id).one()
        except:
            return None
    
    # GET - Retrieve details of a specific company by its ID
    def get(self, request, st_company_id, format=None):
        session = Session()
        try:
            company = self.get_object(st_company_id, session)
            if company is None:
                return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(sqlalchemy_obj_to_dict(company), status=status.HTTP_200_OK)
        finally:
            Session.remove()  # Properly clean up the session
    
    # PUT - Update details of a specific company
    # DELETE - Remove a specific company from the database
    def delete(self, request, st_company_id, format=None):
        session = Session()
        try:
            company = self.get_object(st_company_id, session)
            if company is None:
                return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

            session.delete(company)
            session.commit()
            return Response({'message': 'Company deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()  # Properly clean up the session

# Funding Valuation List View (GET, POST)
class StFundingValuationList(APIView):
    
    # GET - Retrieve all funding valuation records
    def get(self, request, *args, **kwargs):
        session = Session()
        try:
            funding_valuations = session.query(StFundingValuation).all()
            funding_data = [sqlalchemy_obj_to_dict(funding) for funding in funding_valuations]
            return Response(funding_data, status=status.HTTP_200_OK)
        finally:
            Session.remove()  # Properly clean up the session

    def post(self, request, *args, **kwargs):
        session = Session()
        try:
            data = request.data
            new_funding = StFundingValuation(
                st_company_id=data['st_company_id'],
                st_stage=data['st_stage'],
                st_raised_to_date=data['st_raised_to_date'],
                st_last_valuation=data['st_last_valuation'],
                st_current_valuation=data['st_current_valuation'],
                st_capital_requirements=data['st_capital_requirements'],
                st_currency=data.get('st_currency', 'USD'),  # New single currency field
                st_created_by=data.get('st_created_by', 1),  # Assuming default creator id
                st_modified_by=data.get('st_modified_by', 1),  # Assuming default modifier id
                is_active=data.get('is_active', True)
            )
            session.add(new_funding)
            session.commit()
            return Response({'message': 'Funding Valuation created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()  # Properly clean up the session



# Funding Valuation Detail View (GET, PUT, DELETE)
class StFundingValuationDetail(APIView):
    
    # Helper method to get a specific funding valuation by ID
    def get_object(self, st_funding_id, session):
        try:
            return session.query(StFundingValuation).filter(StFundingValuation.st_funding_id == st_funding_id).one()
        except:
            return None
    
    # GET - Retrieve details of a specific funding valuation by its ID
    def get(self, request, st_funding_id, format=None):
        session = Session()
        try:
            funding = self.get_object(st_funding_id, session)
            if funding is None:
                return Response({'error': 'Funding valuation not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(sqlalchemy_obj_to_dict(funding), status=status.HTTP_200_OK)
        finally:
            Session.remove()  # Properly clean up the session
    
    # PUT - Update details of a specific funding valuation
    # DELETE - Remove a specific funding valuation from the database
    def delete(self, request, st_funding_id, format=None):
        session = Session()
        try:
            funding = self.get_object(st_funding_id, session)
            if funding is None:
                return Response({'error': 'Funding valuation not found'}, status=status.HTTP_404_NOT_FOUND)

            session.delete(funding)
            session.commit()
            return Response({'message': 'Funding valuation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()  # Properly clean up the session

# Ownership Structure List View (GET, POST)
class StOwnershipStructureList(APIView):
    
    # GET - Retrieve all ownership structures
    def get(self, request, *args, **kwargs):
        session = Session()
        try:
            ownerships = session.query(StOwnershipStructure).all()
            ownership_data = [sqlalchemy_obj_to_dict(ownership) for ownership in ownerships]
            return Response(ownership_data, status=status.HTTP_200_OK)
        finally:
            Session.remove()

    # POST - Create a new ownership structure entry
    def post(self, request, *args, **kwargs):
        session = Session()
        try:
            data = request.data

            # If it's a list of shareholders, iterate over each one
            if isinstance(data, list):
                for shareholder_data in data:
                    new_ownership = StOwnershipStructure(
                        st_company_id=shareholder_data['st_company_id'],
                        st_type=shareholder_data['st_type'],
                        st_shareholder_name=shareholder_data['st_shareholder_name'],
                        st_holding_percentage=shareholder_data['st_holding_percentage'],
                        is_active=shareholder_data.get('is_active', True)
                    )
                    session.add(new_ownership)
            else:
                # Handle single object
                new_ownership = StOwnershipStructure(
                    st_company_id=data['st_company_id'],
                    st_type=data['st_type'],
                    st_shareholder_name=data['st_shareholder_name'],
                    st_holding_percentage=data['st_holding_percentage'],
                    is_active=data.get('is_active', True)
                )
                session.add(new_ownership)

            session.commit()
            return Response({'message': 'Ownership structure created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()

# Ownership Structure Detail View (GET, PUT, DELETE)
class StOwnershipStructureDetail(APIView):
    
    # Helper method to get a specific ownership structure by ID
    def get_object(self, st_ownership_id, session):
        try:
            return session.query(StOwnershipStructure).filter(StOwnershipStructure.st_ownership_id == st_ownership_id).one()
        except:
            return None
    
    # GET - Retrieve details of a specific ownership structure by its ID
    def get(self, request, st_ownership_id, format=None):
        session = Session()
        try:
            ownership = self.get_object(st_ownership_id, session)
            if ownership is None:
                return Response({'error': 'Ownership structure not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(sqlalchemy_obj_to_dict(ownership), status=status.HTTP_200_OK)
        finally:
            Session.remove()
    
    # PUT - Update details of a specific ownership structu    def put(self, request, st_ownership_id, format=None):

    # DELETE - Remove a specific ownership structure from the database
    def delete(self, request, st_ownership_id, format=None):
        session = Session()
        try:
            ownership = self.get_object(st_ownership_id, session)
            if ownership is None:
                return Response({'error': 'Ownership structure not found'}, status=status.HTTP_404_NOT_FOUND)

            session.delete(ownership)
            session.commit()
            return Response({'message': 'Ownership structure deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()



# Parametric Scoring List View (GET, POST)
# Parametric Scoring List View (GET, POST)
class StParametricScoringList(APIView):
    
    # Helper method to calculate the confidence level
    def calculate_confidence_level(self, scoring):
        # Extract all the relevant scores
        scores = [
            scoring.st_market_potential,
            scoring.st_product_viability,
            scoring.st_financial_health,
            scoring.st_team_strength,
            scoring.st_competitive_advantage,
            scoring.st_customer_traction,
            scoring.st_risk_factors,
            scoring.st_exit_potential,
            scoring.st_innovation,
            scoring.st_sustainability
        ]
        
        # Calculate the average score
        total_score = sum(scores)
        average_score = total_score / len(scores)  # Calculate average
        confidence_level = (average_score / 10) * 100  # Convert to percentage
        return confidence_level

    # GET - Retrieve all parametric scoring records
    def get(self, request, *args, **kwargs):
        session = Session()
        try:
            scorings = session.query(StParametricScoring).all()
            scoring_data = []
            
            # Calculate confidence level for each entry and append to data
            for scoring in scorings:
                scoring_dict = sqlalchemy_obj_to_dict(scoring)
                scoring_dict['confidence_level'] = f"{self.calculate_confidence_level(scoring):.2f}%"
                scoring_data.append(scoring_dict)

            return Response(scoring_data, status=status.HTTP_200_OK)
        finally:
            Session.remove()
    # POST - Create a new parametric scoring record
    def post(self, request, *args, **kwargs):
        session = Session()
        try:
            data = request.data
            new_scoring = StParametricScoring(
                st_company_id=data['st_company_id'],
                st_market_potential=data['st_market_potential'],
                st_product_viability=data['st_product_viability'],
                st_financial_health=data['st_financial_health'],
                st_team_strength=data['st_team_strength'],
                st_competitive_advantage=data['st_competitive_advantage'],
                st_customer_traction=data['st_customer_traction'],
                st_risk_factors=data['st_risk_factors'],
                st_exit_potential=data['st_exit_potential'],
                st_innovation=data['st_innovation'],
                st_sustainability=data['st_sustainability'],
                is_active=data.get('is_active', True)
            )
            session.add(new_scoring)
            session.commit()
            return Response({'message': 'Parametric scoring created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove() 

# Parametric Scoring Detail View (GET, PUT, DELETE)
class StParametricScoringDetail(APIView):
    
    # Helper method to get a specific parametric scoring by ID
    def get_object(self, st_parametric_scoring_id, session):
        try:
            return session.query(StParametricScoring).filter(StParametricScoring.st_parametric_scoring_id == st_parametric_scoring_id).one()
        except:
            return None
    
    # GET - Retrieve details of a specific parametric scoring by its ID
    def get(self, request, st_parametric_scoring_id, format=None):
        session = Session()
        try:
            scoring = self.get_object(st_parametric_scoring_id, session)
            if scoring is None:
                return Response({'error': 'Parametric scoring not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(sqlalchemy_obj_to_dict(scoring), status=status.HTTP_200_OK)
        finally:
            Session.remove()
    
    # PUT - Update details of a specific parametric scoring

    # DELETE - Remove a specific parametric scoring from the database
    def delete(self, request, st_parametric_scoring_id, format=None):
        session = Session()
        try:
            scoring = self.get_object(st_parametric_scoring_id, session)
            if scoring is None:
                return Response({'error': 'Parametric scoring not found'}, status=status.HTTP_404_NOT_FOUND)

            session.delete(scoring)
            session.commit()
            return Response({'message': 'Parametric scoring deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            Session.remove()


#
class CombinedFormSubmission(APIView):

    def post(self, request, *args, **kwargs):
        session = Session()
        try:
            data = request.data  # This will contain data for all forms

            # Company Overview Form data
            new_company = StCompanyOverview(
                st_company_name=data['company_overview']['st_company_name'],
                st_company_description=data['company_overview']['st_company_description'],
                st_year_of_incorporation=data['company_overview']['st_year_of_incorporation'],
                st_country=data['company_overview']['st_country'],
                st_total_founders=data['company_overview']['st_total_founders'],
                st_no_of_employees=data['company_overview']['st_no_of_employees'],
                st_founder_names=data['company_overview']['st_founder_names'],
                st_industry_type=data['company_overview']['st_industry_type'],
                st_geography=data['company_overview']['st_geography'],
                is_active=data['company_overview'].get('is_active', True)
            )
            session.add(new_company)
            session.flush()  # Flush to get the company ID for other forms

            # Funding Valuation Form data
            funding_data = data.get('funding_valuation', {})
            new_funding = StFundingValuation(
                st_company_id=new_company.st_company_id,  # Linking to company
                st_stage=funding_data.get('st_stage'),
                st_raised_to_date=funding_data.get('st_raised_to_date'),  # Now expecting string
                st_last_valuation=funding_data.get('st_last_valuation'),  # Now expecting string
                st_current_valuation=funding_data.get('st_current_valuation'),  # Now expecting string
                st_capital_requirements=funding_data.get('st_capital_requirements'),  # Now expecting string
                st_currency=funding_data.get('st_currency', 'USD'),  # Default currency
                is_active=funding_data.get('is_active', True)
            )
            session.add(new_funding)

            # Ownership Structure Form data (Multiple shareholders possible)
            ownership_data = data.get('ownership_structure', [])
            for shareholder in ownership_data:
                new_ownership = StOwnershipStructure(
                    st_company_id=new_company.st_company_id,
                    st_type=shareholder['st_type'],
                    st_shareholder_name=shareholder['st_shareholder_name'],
                    st_holding_percentage=shareholder['st_holding_percentage'],
                    is_active=shareholder.get('is_active', True)
                )
                session.add(new_ownership)

            # Parametric Scoring Form data
            scoring_data = data.get('parametric_scoring', {})
            new_scoring = StParametricScoring(
                st_company_id=new_company.st_company_id,
                st_market_potential=scoring_data.get('st_market_potential'),
                st_product_viability=scoring_data.get('st_product_viability'),
                st_financial_health=scoring_data.get('st_financial_health'),
                st_team_strength=scoring_data.get('st_team_strength'),
                st_competitive_advantage=scoring_data.get('st_competitive_advantage'),
                st_customer_traction=scoring_data.get('st_customer_traction'),
                st_risk_factors=scoring_data.get('st_risk_factors'),
                st_exit_potential=scoring_data.get('st_exit_potential'),
                st_innovation=scoring_data.get('st_innovation'),
                st_sustainability=scoring_data.get('st_sustainability'),
                is_active=scoring_data.get('is_active', True)
            )
            session.add(new_scoring)

            # Commit all changes
            session.commit()
            return Response({'message': 'Forms submitted successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            session.rollback()  # Rollback in case of error
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()  # Properly close the session

    def get(self, request, *args, **kwargs):
        session = Session()
        try:
            # Retrieve the most recently created company
            latest_company = session.query(StCompanyOverview).order_by(StCompanyOverview.st_company_id.desc()).first()
            if not latest_company:
                return Response({'error': 'No companies found'}, status=status.HTTP_404_NOT_FOUND)

            # Fetch related details using the latest company ID
            funding_valuation = session.query(StFundingValuation).filter_by(st_company_id=latest_company.st_company_id).first()
            ownership_structure = session.query(StOwnershipStructure).filter_by(st_company_id=latest_company.st_company_id).all()
            parametric_scoring = session.query(StParametricScoring).filter_by(st_company_id=latest_company.st_company_id).first()

            # Prepare the response data
            company_details = {
                'st_company_id': latest_company.st_company_id,  # Include the latest company ID here
                'company_overview': {
                    'st_company_name': latest_company.st_company_name,
                    'st_company_description': latest_company.st_company_description,
                    'st_year_of_incorporation': latest_company.st_year_of_incorporation,
                    'st_country': latest_company.st_country,
                    'st_total_founders': latest_company.st_total_founders,
                    'st_no_of_employees': latest_company.st_no_of_employees,
                    'st_founder_names': latest_company.st_founder_names,
                    'st_industry_type': latest_company.st_industry_type,
                    'st_geography': latest_company.st_geography,
                    'is_active': latest_company.is_active
                },
                'funding_valuation': {
                    'st_stage': funding_valuation.st_stage if funding_valuation else None,
                    'st_raised_to_date': funding_valuation.st_raised_to_date if funding_valuation else None,
                    'st_last_valuation': funding_valuation.st_last_valuation if funding_valuation else None,
                    'st_current_valuation': funding_valuation.st_current_valuation if funding_valuation else None,
                    'st_capital_requirements': funding_valuation.st_capital_requirements if funding_valuation else None,
                    'st_currency': funding_valuation.st_currency if funding_valuation else None,
                    'is_active': funding_valuation.is_active if funding_valuation else None
                },
                'ownership_structure': [
                    {
                        'st_type': own.st_type,
                        'st_shareholder_name': own.st_shareholder_name,
                        'st_holding_percentage': own.st_holding_percentage,
                        'is_active': own.is_active
                    } for own in ownership_structure
                ],
                'parametric_scoring': {
                    'st_market_potential': parametric_scoring.st_market_potential if parametric_scoring else None,
                    'st_product_viability': parametric_scoring.st_product_viability if parametric_scoring else None,
                    'st_financial_health': parametric_scoring.st_financial_health if parametric_scoring else None,
                    'st_team_strength': parametric_scoring.st_team_strength if parametric_scoring else None,
                    'st_competitive_advantage': parametric_scoring.st_competitive_advantage if parametric_scoring else None,
                    'st_customer_traction': parametric_scoring.st_customer_traction if parametric_scoring else None,
                    'st_risk_factors': parametric_scoring.st_risk_factors if parametric_scoring else None,
                    'st_exit_potential': parametric_scoring.st_exit_potential if parametric_scoring else None,
                    'st_innovation': parametric_scoring.st_innovation if parametric_scoring else None,
                    'st_sustainability': parametric_scoring.st_sustainability if parametric_scoring else None,
                    'is_active': parametric_scoring.is_active if parametric_scoring else None
                }
            }

            return Response(company_details, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()  # Properly close the session

