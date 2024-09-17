from django.urls import path
from .views import CombinedFormSubmission
#CombinedFormSubmission.as_view()from django.urls import path
from .views import (
    StCompanyOverviewList, 
    StCompanyOverviewDetail, 
    StFundingValuationList, 
    StFundingValuationDetail,
    StOwnershipStructureList, StOwnershipStructureDetail, StParametricScoringList, StParametricScoringDetail,CombinedFormSubmission
)

urlpatterns = [
    # Company Overview List - For listing all companies and creating a new one
    path('company-overview', StCompanyOverviewList.as_view(), name='company-overview-list'),
    
    # Company Overview Detail - For retrieving, updating, or deleting a specific company by ID
    path('company-overview/<int:st_company_id>/', StCompanyOverviewDetail.as_view(), name='company-overview-detail'),

    # Funding Valuation List - For listing all funding records and creating a new one
    path('funding-valuation', StFundingValuationList.as_view(), name='funding-valuation-list'),

    # Funding Valuation Detail - For retrieving, updating, or deleting a specific funding valuation by ID
    path('funding-valuation/<int:st_funding_id>/', StFundingValuationDetail.as_view(), name='funding-valuation-detail'),


        # Ownership Structure
    path('ownership-structure', StOwnershipStructureList.as_view(), name='ownership-structure-list'),
    path('ownership-structure/<int:st_ownership_id>/', StOwnershipStructureDetail.as_view(), name='ownership-structure-detail'),

    # Parametric Scoring
    path('api/v1/parametric-scoring/', StParametricScoringList.as_view(), name='parametric-scoring-list'),
    path('parametric-scoring/<int:st_parametric_scoring_id>/', StParametricScoringDetail.as_view(), name='parametric-scoring-detail'),
    path('api/v1/submit-all-forms/', CombinedFormSubmission.as_view(), name='submit_all_forms'),
#    path('submit-all-forms', CombinedFormSubmission.as_view(), name='submit_all_forms'),
]
