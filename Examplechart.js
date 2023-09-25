import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

window.d3 = d3
window.Plot = Plot

function extractFundingData(idSelector) {
    let table = d3.select(`${idSelector} table`)

    let xs = []
    table.selectAll("thead tr th[colspan='3']").each(function() {
        xs.push(d3.select(this).text())
    })

    let data = []

    let spCumulativeTotal = 0
    let oCumulativeTotal = 0
    let eCumulativeTotal = 0

    let totals = d3.select(`${idSelector} table`).selectAll(".bottom-line-total").nodes()

    if(totals.length) {
        for(let i = 0, j = 0; i < 12; i += 3, j++){
            let c = totals.slice(i, i + 3)

            let sp = parseFloat(c[0].textContent)
            spCumulativeTotal += sp

            let o = parseFloat(c[1].textContent)
            oCumulativeTotal += o

            let e = parseFloat(c[2].textContent)
            eCumulativeTotal += e

            data.push({ fiscal_quarter: xs[j], type: "Spend Plan", total: sp, cumulative_total: spCumulativeTotal })
            data.push({ fiscal_quarter: xs[j], type: "Obligations", total: o, cumulative_total: oCumulativeTotal })
            data.push({ fiscal_quarter: xs[j], type: "Expenditures", total: e, cumulative_total: eCumulativeTotal })
        }
    }

    return data
}

const formatDollars = d3.format("$,.2f")

function renderGraph(data) {
    let graph = Plot.plot({
        width: 720,
        insetBottom: 10,
        marginLeft: 50,
        color: {
            legend: true,
            scheme: "Tableau10",
            domain: ["Spend Plan", "Obligations", "Expenditures"]
        },
        x: {
            label: null,
        },
        y: {
            grid: true,
            label: "↑ Dollars in Thousands",
            tickFormat: "$,f",
            nice: true,
            line: true,
        },
        marks: [
            Plot.line(data, {
                x: "fiscal_quarter", y: "cumulative_total", stroke: "type", strokeWidth: 2}),
            Plot.dot(data, {
                x: "fiscal_quarter", y: "cumulative_total", r: 4, fill: "type", tip: true,
                title: (d) => `${d.type} - ${d.fiscal_quarter} \n ${formatDollars(d.cumulative_total)}`
            }),
        ]
    })

    return graph
}

function renderBarChart(data) {
    let bar = Plot.plot({
        width: 720,
        height: 470,
        marginRight: 60,
        marginTop: 0,
        x: {
            grid: true,
            label: "Dollars in Thousands →",
            tickFormat: "$,f",
            nice: true,
            line: true,
        },
        y: {
            axis: null
        },
        fy: {
            label: null
        },
        color : {
            scheme: "Tableau10",
            domain: ["Spend Plan", "Obligations", "Expenditures"]
        },
        marks: [
            Plot.barX(data, {
                x: "total", y: "type", fy: "fiscal_quarter", fill: "type", sort: { y: "y", reverse: true},
                title: (d) => `${d.type} - ${d.fiscal_quarter} \n ${formatDollars(d.total)}`
            }),
            Plot.text(data, {
                x: "total", y: "type", fy: "fiscal_quarter", text: (d) => `${formatDollars(d.total)}`,
                textAnchor: "start", dx: 4
            })
        ]
    })

    return bar
}

document.addEventListener("DOMContentLoaded", () => {
    if(document.querySelector("****-plots")) {
        let ****_data = extractFundingData("#nip-funding")

        document.querySelector("****-funding-graph").append(renderGraph(****_data))
        document.querySelector("****-funding-bar").append(renderBarChart(****_data))
    }

    if(document.querySelector("****-plots")) {
        let ****_data = extractFundingData("*****-funding")

        document.querySelector("****-funding-graph").append(renderGraph(****_data))
        document.querySelector("****-funding-bar").append(renderBarChart(****_data))
    }
})
