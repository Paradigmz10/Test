class ProgramDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Program
    context_object_name = "program"
    permission_required = ("*****.view_program",)
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related().prefetch_related()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        pmrs = self.object.program_management_review_set.select_related().order_by(
            "-fiscal_quarter__year", "-fiscal_quarter__number"
        )

        if user.is_member(authorization.constants.*****):
            pmrs = pmrs.exclude(status=ProgramManagementReview.Status.IN_PROGRESS)

        context["program_management_reviews"] = pmrs

        context["service_assessments"] = (
            ServiceAssessment.objects.select_related()
            .filter(program_management_review__in=pmrs)
            .order_by(
                "-program_management_review__fiscal_quarter__year",
                "-program_management_review__fiscal_quarter__number",
            )[:4]
        )

        context["architecture_compliance_assessments"] = (
            ArchitectureComplianceAssessment.objects.select_related()
            .filter(program_management_review__in=pmrs)
            .order_by(
                "-program_management_review__fiscal_quarter__year",
                "-program_management_review__fiscal_quarter__number",
            )[:4]
        )

        if pmrs:
            last_pmr = pmrs.first()
            context["last_pmr"] = last_pmr

            if hasattr(last_pmr, "financial_assessment"):
                last_pmr_funding_profile_funding = last_pmr.financial_assessment.funding_profile_funding_set.select_related().order_by(
                    "fiscal_year"
                )

                last_pmr_funding_profile_funding_nip_only = (
                    last_pmr_funding_profile_funding.filter(
                        funding_type=FundingTypeChoice.NIP
                    )
                )

                if last_pmr_funding_profile_funding_nip_only.exists():
                    context[
                        "last_pmr_funding_profile_funding_nip_only"
                    ] = last_pmr_funding_profile_funding_nip_only

                    context[
                        "last_pmr_nip_funding_profile_funding"
                    ] = funding_profile_funding_reshape_and_add_total(
                        last_pmr_funding_profile_funding_nip_only
                    )

                last_pmr_funding_profile_funding_mip_only = (
                    last_pmr_funding_profile_funding.filter(
                        funding_type=FundingTypeChoice.MIP
                    )
                )

                if last_pmr_funding_profile_funding_mip_only.exists():
                    context[
                        "last_pmr_funding_profile_funding_mip_only"
                    ] = last_pmr_funding_profile_funding_mip_only

                    context[
                        "last_pmr_mip_funding_profile_funding"
                    ] = funding_profile_funding_reshape_and_add_total(
                        last_pmr_funding_profile_funding_mip_only
                    )

            context["accomplishments"] = last_pmr.accomplishment_set.order_by(
                "created_at"
            )

            context["open_action_items"] = last_pmr.action_item_set.open().order_by(
                "priority"
            )

            open_risks = last_pmr.risk_set.open().order_by("-score")
            context["open_risks"] = open_risks
            context["risk_matrix"] = risk_matrix(open_risks)

        return context
