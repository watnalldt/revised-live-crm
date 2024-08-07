from django.contrib import admin
from django.db.models import Q


class CustomSearchAdmin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        """
        Enhances filtering by allowing searches for multiple MPAN numbers separated by commas,
        and maintains compatibility with other applied filters.
        """
        use_distinct = False
        # Check if the search_term involves potential multiple MPAN numbers
        if "," in search_term:
            mpan_terms = [term.strip() for term in search_term.split(",") if term.strip()]
            if mpan_terms:
                q_objects = Q(mpan_mpr__iexact=mpan_terms[0])  # Start with the first term
                for term in mpan_terms[1:]:
                    q_objects |= Q(mpan_mpr__iexact=term)  # Use |= to add each subsequent term
                queryset = queryset.filter(q_objects).distinct()
                use_distinct = True
        else:
            # Handle single mpan_mpr or other search fields via superclass method
            queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
