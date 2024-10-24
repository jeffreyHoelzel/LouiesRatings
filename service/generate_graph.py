import altair as alt
import pandas as pd

GRADE_COLUMN_NAMES = ['a', 'b', 'c', 'd', 'f', 'au', 'p', 'ng', 'w', 'i', 'ip', 'pending']

# get dataframe (could be for professor or class)
# just graph the grades
example_df = pd.DataFrame({
    "Class": ["CS 112", "CS 212", "CS 312"],
    "Section": ["001", "001", "001"],
    "Class NBR ": [1640, 2947, 2949],
    "Instructor Name": ["Otte,Wolf-Dieter Wilhelm", "Gali,Veera Surya Bhaskar", "Gali,Veera Surya Bhaskar"],
    "A": [15, 18, 32],
    "B": [8, 0, 1],
    "C": [1, 0, 0],
    "D": [0, 0, 0],
    "F": [0, 1, 2],
    "AU": [0, 0, 0],
    "P": [0, 0, 0],
    "NG": [0, 0, 0],
    "W": [1, 1, 1],
    "I": [0, 0, 0],
    "IP": [0, 0, 0],
    "Pending": [0, 0, 0],
    "Total": [25, 20, 36]
})

# creates graph as json
# class_data: pandas df that has column names for a, b , c, d, f, au , p, ng, w, i, ip, they can be upper or lower case
def make_graph(class_data: pd.DataFrame):
    # make all column names lower case
    class_data.columns = class_data.columns.str.lower()

    # extract only the grade distributions
    grade_distributions = class_data.filter(items=GRADE_COLUMN_NAMES)

    # add row for column sums
    grade_distributions.loc["sum"] = grade_distributions.sum(numeric_only=True)

    # remove all rows except for the last two
    grade_distributions = grade_distributions.iloc[[-1]]

    # transpose, and make the index a column for grades
    grade_distributions = grade_distributions.T.reset_index(drop=False).rename(columns={"index":"grade"})

    # create the chart
    chart = alt.Chart(grade_distributions).mark_bar().encode(
        x=alt.X(
            "grade:N", 
            sort=None,
            title=None
            ),
        y=alt.Y(
            "sum:Q",
            title=None
            ),
        color=alt.value("#002454")
    )

    return chart.save('chart.json')

if __name__ == "__main__":
    make_graph(example_df)