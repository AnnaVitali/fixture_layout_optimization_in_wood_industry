# Fixtures Layout Optimization

This project contains the two Minzinc models made for the fixture layout optimization problem, with reference to #TODO article

## Project Structure

- `minizinc/`: Directory containing the two Minzinc model implemented.
- `resources/`: Directory containing input JSON files with the results of the executed model.
- `src/plot_fdist_result.py`: Script to display results for the _f\_dist_ objective function.
- `src/plot_finer_result.py`: Script to display results for the _f\_iner_ objective function.


## Run the example

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fixtures_layout_optimization.git
   cd fixtures_layout_optimization
   
2. Open one of the two Minzinc models in the Minzinc IDE.
3. Copy the result obtained in the corresponding JSON file in the `resources/` directory.
4. Run the script to display the results:
   ```bash
   python src/plot_fdist_result.py
   ```
   or
   ```bash
   python src/plot_finer_result.py
   ```