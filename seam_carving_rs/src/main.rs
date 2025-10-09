use anyhow::{Context, Result, anyhow};
use image::{DynamicImage, ImageBuffer, Pixel, Rgb};
use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq)]
struct SeamStep {
    col: usize,
    row: usize,
}

fn main() -> Result<()> {
    // Configuration - change these values as needed
    let image_name = "tower.jpg";
    let num_vertical_seams = 600;

    // Dynamic path construction based on project directory
    // CARGO_MANIFEST_DIR is the directory containing Cargo.toml
    let project_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let input_path = project_dir.join(image_name);
    let output_path =
        project_dir.join(format!("seam_carved_{}_{}", num_vertical_seams, image_name));

    println!("Input: {}", input_path.display());
    println!("Output: {}", output_path.display());
    println!("Removing {} vertical seams", num_vertical_seams);

    let image = image::open(&input_path)
        .with_context(|| format!("Failed to open image at {}", input_path.display()))?;

    let rgb_image = image.to_rgb8();

    let carved = carve_vertical_seams(rgb_image, num_vertical_seams)
        .with_context(|| "Failed to carve seams")?;

    DynamicImage::ImageRgb8(carved)
        .save(&output_path)
        .with_context(|| format!("Failed to save image at {}", output_path.display()))?;

    println!(
        "Successfully saved carved image to {}",
        output_path.display()
    );

    Ok(())
}

fn carve_vertical_seams(
    mut image: ImageBuffer<Rgb<u8>, Vec<u8>>,
    seams_to_remove: usize,
) -> Result<ImageBuffer<Rgb<u8>, Vec<u8>>> {
    for seam_index in 0..seams_to_remove {
        println!("Removing seam {}/{}", seam_index + 1, seams_to_remove);

        let weights = compute_energy_weights(&image);
        let seam = find_min_seam_path(&weights);

        image = remove_vertical_seam(&image, &seam)?;
    }

    Ok(image)
}

fn compute_energy_weights(image: &ImageBuffer<Rgb<u8>, Vec<u8>>) -> Vec<Vec<u32>> {
    let (width, height) = image.dimensions();
    let mut weights = vec![vec![0u32; width as usize]; height as usize];

    for y in 0..height {
        for x in 0..width {
            let weight = sobel_energy(image, x as i32, y as i32);
            weights[y as usize][x as usize] = weight;
        }
    }

    weights
}

fn sobel_energy(image: &ImageBuffer<Rgb<u8>, Vec<u8>>, x: i32, y: i32) -> u32 {
    const SOBEL_KERNEL: [[i32; 3]; 3] = [[1, 0, -1], [2, 0, -2], [1, 0, -1]];

    // Apply filter to each channel separately, then sum (like PIL does)
    let mut channel_sums = [0i32; 3];

    for ky in 0..3 {
        for kx in 0..3 {
            let pixel_x = (x + kx - 1).clamp(0, image.width() as i32 - 1);
            let pixel_y = (y + ky - 1).clamp(0, image.height() as i32 - 1);
            let pixel = image.get_pixel(pixel_x as u32, pixel_y as u32);

            let coeff = SOBEL_KERNEL[ky as usize][kx as usize];

            // Apply coefficient to each channel separately
            for (i, &channel_value) in pixel.channels().iter().enumerate() {
                channel_sums[i] += coeff * (channel_value as i32);
            }
        }
    }

    // Sum the absolute values of each channel's result
    channel_sums.iter().map(|&v| v.unsigned_abs()).sum()
}

fn find_min_seam_path(weights: &[Vec<u32>]) -> Vec<SeamStep> {
    let rows = weights.len();
    if rows == 0 {
        return Vec::new();
    }
    let cols = weights[0].len();
    if cols == 0 {
        return Vec::new();
    }

    if rows == 1 {
        let min_col = weights[0]
            .iter()
            .enumerate()
            .min_by_key(|(_, w)| *w)
            .map(|(col, _)| col)
            .unwrap_or(0);
        return vec![SeamStep {
            col: min_col,
            row: 0,
        }];
    }

    if cols == 1 {
        return (0..rows).map(|row| SeamStep { col: 0, row }).collect();
    }

    let mut memo = vec![vec![0u32; cols]; rows];
    memo[0].clone_from_slice(&weights[0]);

    for row in 1..rows {
        for col in 0..cols {
            let mut min_cost = memo[row - 1][col];
            if col > 0 {
                min_cost = min_cost.min(memo[row - 1][col - 1]);
            }
            if col + 1 < cols {
                min_cost = min_cost.min(memo[row - 1][col + 1]);
            }
            memo[row][col] = weights[row][col] + min_cost;
        }
    }

    let mut seam = vec![
        SeamStep {
            col: 0,
            row: rows - 1
        };
        rows
    ];
    let mut current_col = memo[rows - 1]
        .iter()
        .enumerate()
        .min_by_key(|(_, cost)| *cost)
        .map(|(col, _)| col)
        .unwrap_or(0);

    seam[rows - 1] = SeamStep {
        col: current_col,
        row: rows - 1,
    };

    for row in (0..rows - 1).rev() {
        let mut current_cost = memo[row][current_col];
        let mut best_col = current_col;

        if current_col > 0 {
            let left_cost = memo[row][current_col - 1];
            if left_cost < current_cost {
                current_cost = left_cost;
                best_col = current_col - 1;
            }
        }

        if current_col + 1 < cols {
            let right_cost = memo[row][current_col + 1];
            if right_cost < current_cost {
                best_col = current_col + 1;
            }
        }

        current_col = best_col;

        seam[row] = SeamStep {
            col: current_col,
            row,
        };
    }

    seam
}

fn remove_vertical_seam(
    image: &ImageBuffer<Rgb<u8>, Vec<u8>>,
    seam: &[SeamStep],
) -> Result<ImageBuffer<Rgb<u8>, Vec<u8>>> {
    let (width, height) = image.dimensions();
    if width <= 1 {
        return Err(anyhow!("Cannot remove seam from image with width <= 1"));
    }

    if seam.len() != height as usize {
        return Err(anyhow!(
            "Seam length ({}) does not match image height ({})",
            seam.len(),
            height
        ));
    }

    let mut new_image = ImageBuffer::new(width - 1, height);

    for (row, step) in seam.iter().enumerate() {
        if step.row != row {
            return Err(anyhow!("Seam row mismatch at row {}", row));
        }
        if step.col >= width as usize {
            return Err(anyhow!(
                "Seam column {} out of bounds for width {}",
                step.col,
                width
            ));
        }

        for col in 0..step.col {
            let pixel = image.get_pixel(col as u32, row as u32);
            new_image.put_pixel(col as u32, row as u32, *pixel);
        }

        for col in step.col + 1..width as usize {
            let pixel = image.get_pixel(col as u32, row as u32);
            new_image.put_pixel((col - 1) as u32, row as u32, *pixel);
        }
    }

    Ok(new_image)
}
