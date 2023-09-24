from .models import AppropriationCategoryChoice


def funding_profile_funding_reshape_and_add_total(funding_set=None):
    if funding_set is None or not funding_set.exists():
        return []

    funding = {}

    for f in funding_set:
        year = str(f.fiscal_year)
        if year not in funding:
            funding[year] = {"rdte": 0, "proc": 0, "o_and_m": 0, "delta": 0}

        funding[year]["rdte"] += f.rdte
        funding[year]["proc"] += f.proc
        funding[year]["o_and_m"] += f.o_and_m
        funding[year]["delta"] += f.delta

    sorted_funding = dict(sorted(funding.items()))

    fpf = [list(sorted_funding.keys())]

    acf = []
    acf.extend(sorted_funding[key]["rdte"] for key in sorted_funding.keys())
    acf.append(sum(acf))
    fpf.append(acf)

    acf = []
    acf.extend(sorted_funding[key]["proc"] for key in sorted_funding.keys())
    acf.append(sum(acf))
    fpf.append(acf)

    acf = []
    acf.extend(sorted_funding[key]["o_and_m"] for key in sorted_funding.keys())
    acf.append(sum(acf))
    fpf.append(acf)

    fpf.append(
        [sum([fpf[x][y] for x in range(1, 4)]) for y in range(0, len(fpf[0]) + 1)]
    )

    acf = []
    acf.extend(sorted_funding[key]["delta"] for key in sorted_funding.keys())
    acf.append(sum(filter(None, acf)))
    fpf.append(acf)

    return fpf


def funding_profile_funding_subcategories(funding_set):
    funding = {}
    years = {}

    for f in funding_set:
        subcategory_name = f.nip_program_subcategory.name
        if subcategory_name not in funding:
            funding[subcategory_name] = {}

        year = str(f.fiscal_year)
        years[year] = True
        if year not in funding[subcategory_name]:
            funding[subcategory_name][year] = {"rdte": 0, "proc": 0, "o_and_m": 0}

        sub = funding[subcategory_name][year]

        sub["rdte"] += f.rdte
        sub["proc"] += f.proc
        sub["o_and_m"] += f.o_and_m

    # Fill in empty years
    for subcategory in funding.values():
        subcategory["total"] = {"rdte": 0, "proc": 0, "o_and_m": 0}

        for year in years.keys():
            if year not in subcategory:
                subcategory[year] = {"rdte": 0, "proc": 0, "o_and_m": 0}
            else:
                subcategory["total"]["rdte"] += subcategory[year]["rdte"]
                subcategory["total"]["proc"] += subcategory[year]["proc"]
                subcategory["total"]["o_and_m"] += subcategory[year]["o_and_m"]

    return dict(sorted(funding.items()))


def reshape_and_add_totals(
    program_management_review=None,
    funding_set=None,
    funding_type=None,
    previous_two_fiscal_years=None,
):
    if (
        program_management_review is None
        or funding_set is None
        or funding_type is None
        or previous_two_fiscal_years is None
    ):
        return []

    fiscal_quarters = (
        program_management_review.fiscal_quarter.fiscal_year.fiscal_quarters.all()
    )
    appropriation_categories = AppropriationCategoryChoice.choices

    funding = [[None for _y in fiscal_quarters] for _x in appropriation_categories]
    for x, ac in enumerate(appropriation_categories):
        for y, fq in enumerate(fiscal_quarters):
            qf = next(
                (
                    qf
                    for qf in funding_set
                    if qf.appropriation_category == ac[0]
                    and qf.fiscal_quarter == fq
                    and qf.funding_type == funding_type
                    and not qf.carryover
                ),
                None,
            )
            if qf:
                funding[x][y] = qf
        funding[x].append(
            [
                sum([qf.spend_plan for qf in filter(None, funding[x][:4])]),
                sum(
                    [
                        qf.obligations
                        for qf in filter(
                            lambda i: i is not None and i.obligations is not None,
                            funding[x][:4],
                        )
                    ]
                ),
                sum(
                    [
                        qf.expenditures
                        for qf in filter(
                            lambda i: i is not None and i.expenditures is not None,
                            funding[x][:4],
                        )
                    ]
                ),
            ]
        )

    funding_transpose = list(zip(*funding))
    funding.append([None for _ in range(0, 15)])
    y = 0
    for x in range(0, 4):
        funding[3][y] = sum(
            [qf.spend_plan for qf in filter(None, funding_transpose[x])]
        )
        y += 1
        funding[3][y] = sum(
            [
                qf.obligations
                for qf in filter(
                    lambda i: i is not None and i.obligations is not None,
                    funding_transpose[x],
                )
            ]
        )
        y += 1
        funding[3][y] = sum(
            [
                qf.expenditures
                for qf in filter(
                    lambda i: i is not None and i.expenditures is not None,
                    funding_transpose[x],
                )
            ]
        )
        y += 1

    totals = list(zip(*funding_transpose[4]))
    funding[3][12] = sum([t for t in totals[0]])
    funding[3][13] = sum([t for t in totals[1]])
    funding[3][14] = sum([t for t in totals[2]])

    carryover_funding = []
    if previous_two_fiscal_years:
        carryover_funding = [
            [None for _y in fiscal_quarters]
            for _x in range(0, len(previous_two_fiscal_years) + 2)
        ]
        for x, fy in enumerate(previous_two_fiscal_years):
            for y, fq in enumerate(fy.fiscal_quarters.all()):
                if x == 0:
                    qf = next(
                        (
                            qf
                            for qf in funding_set
                            if qf.appropriation_category
                            == AppropriationCategoryChoice.RDTE
                            and qf.fiscal_quarter == fq
                            and qf.funding_type == funding_type
                            and qf.carryover
                        ),
                        None,
                    )
                    if qf:
                        carryover_funding[x][y] = qf

                if x == 0:
                    qf = next(
                        (
                            qf
                            for qf in funding_set
                            if qf.appropriation_category
                            == AppropriationCategoryChoice.OM
                            and qf.fiscal_quarter == fq
                            and qf.funding_type == funding_type
                            and qf.carryover
                        ),
                        None,
                    )
                    if qf:
                        carryover_funding[x + 1][y] = qf

                qf = next(
                    (
                        qf
                        for qf in funding_set
                        if qf.appropriation_category == AppropriationCategoryChoice.PROC
                        and qf.fiscal_quarter == fq
                        and qf.funding_type == funding_type
                        and qf.carryover
                    ),
                    None,
                )
                if qf:
                    carryover_funding[x + 2][y] = qf

            if x == 0:
                carryover_funding[x].append(
                    [
                        sum(
                            [
                                qf.spend_plan
                                for qf in filter(None, carryover_funding[x][:4])
                            ]
                        ),
                        sum(
                            [
                                qf.obligations
                                for qf in filter(None, carryover_funding[x][:4])
                            ]
                        ),
                        sum(
                            [
                                qf.expenditures
                                for qf in filter(None, carryover_funding[x][:4])
                            ]
                        ),
                    ]
                )

                carryover_funding[x + 1].append(
                    [
                        sum(
                            [
                                qf.spend_plan
                                for qf in filter(None, carryover_funding[x + 1][:4])
                            ]
                        ),
                        sum(
                            [
                                qf.obligations
                                for qf in filter(None, carryover_funding[x + 1][:4])
                            ]
                        ),
                        sum(
                            [
                                qf.expenditures
                                for qf in filter(None, carryover_funding[x + 1][:4])
                            ]
                        ),
                    ]
                )

            carryover_funding[x + 2].append(
                [
                    sum(
                        [
                            qf.spend_plan
                            for qf in filter(None, carryover_funding[x + 2][:4])
                        ]
                    ),
                    sum(
                        [
                            qf.obligations
                            for qf in filter(None, carryover_funding[x + 2][:4])
                        ]
                    ),
                    sum(
                        [
                            qf.expenditures
                            for qf in filter(None, carryover_funding[x + 2][:4])
                        ]
                    ),
                ]
            )

        carryover_funding_transpose = list(zip(*carryover_funding))
        carryover_funding.append([None for _ in range(0, 15)])
        y = 0
        for x in range(0, 4):
            carryover_funding[-1][y] = sum(
                [qf.spend_plan for qf in filter(None, carryover_funding_transpose[x])]
            )
            y += 1
            carryover_funding[-1][y] = sum(
                [qf.obligations for qf in filter(None, carryover_funding_transpose[x])]
            )
            y += 1
            carryover_funding[-1][y] = sum(
                [qf.expenditures for qf in filter(None, carryover_funding_transpose[x])]
            )
            y += 1

        totals = list(zip(*carryover_funding_transpose[4]))
        carryover_funding[-1][12] = sum([t for t in totals[0]])
        carryover_funding[-1][13] = sum([t for t in totals[1]])
        carryover_funding[-1][14] = sum([t for t in totals[2]])

    # bottom line calculations
    if carryover_funding:
        bottomline_funding = [[None for _ in range(0, 15)]]
        for x in range(0, 15):
            bottomline_funding[0][x] = sum([funding[-1][x], carryover_funding[-1][x]])

        funding += carryover_funding

    else:
        bottomline_funding = [funding[-1]]

    funding += bottomline_funding

    return funding


def risk_matrix(risks=None):
    risk_matrix = [[[] for _i in range(5)] for _j in range(5)]

    for risk in risks:
        risk_matrix[risk.likelihood - 1][risk.impact - 1].append(risk)

    return risk_matrix
