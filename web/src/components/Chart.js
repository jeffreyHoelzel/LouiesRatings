import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis } from 'recharts';
import '../styles/main.css';

const Chart = ({className, instructorName, searchBy}) => {
    const [data, setData] = useState([{grade: "empty", sum:0}]); // Initialize data that is graphed as empty
    const [options, setOptions] = useState(["All"]);
    const [currOption, setCurrOption] = useState("All");

    // fetch options
    useEffect(() => {
        const fetchOptions = async () => {
            const backendUrl = "/service/get_graph_options";

            try {
                // fetch data via class name
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        class_name: className, 
                        instructor_name: instructorName, 
                        search_by: searchBy
                    })
                });
        
                if( response.ok ) {
                    const data = await response.json();
                    setOptions(data)
                }
                else {
                    throw new Error('Fetching chart data was response unsuccessful');
                }

            } catch (error) {
                console.error('There was a problem with fetching chart data:', error);
            }
        };

        fetchOptions();
    }, [])

    // fetch chart data, run whenever option changes
    useEffect(() => {
        const fetchData = async () => {
            const backendUrl = "/service/get_graph_data";

            try {
                // fetch data via class name
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        class_name: className, 
                        instructor_name: instructorName, 
                        search_by: searchBy,
                        option: currOption 
                    })
                });
        
                if( response.ok ) {
                    // fill chart with fetched data
                    const tempData = await response.json();
                    const chartData = JSON.parse(tempData);
                    setData(chartData)
                }
                else {
                    throw new Error('Fetching chart data was response unsuccessful');
                }

            } catch (error) {
                console.error('There was a problem with fetching chart data:', error);
            }
        };

        fetchData();
    }, [currOption]);

    return (
        <div className="grade-distribution-chart">
            <BarChart width={450} height={300} data={data}>
                <Bar dataKey="sum" fill="#002454" />
                <XAxis dataKey="grade" />
                <YAxis />
            </BarChart>

            <div className="chart-dropdown">
                <select value={currOption} onChange={(e) => setCurrOption(e.target.value)}>
                    {options.map((option) => (
                        <option value={option}>{option}</option>
                    ))}
                </select>
            </div>
        </div>
    );
};

export default Chart;