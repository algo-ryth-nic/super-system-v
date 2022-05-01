import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import heroImg from "../../asset/img/hero.png";
export default function Homepage() {
    return (
        <Box sx={{ flexGrow: 1 }} m={2} pt={3}>
            <Grid container maxWidth={"lg"}>
                <Grid item xs={6} md={8}>
                    <Paper>
                        <Container maxWidth="sm">
                            <div style={{ marginTop: 50 }}>
                                <Typography
                                    fontWeight="500"
                                    variant="h3"
                                    component="h2"
                                    align="center"
                                >
                                    Super System V
                                </Typography>
                                <Typography
                                    variant="h5"
                                    component="p"
                                    
                                >
                                    boost sales record 
                                </Typography>
                            </div>
                        </Container>
                    </Paper>
                </Grid>
                <Grid item xs={6} md={4}>
                    <Paper>
                        <img src={heroImg} alt="HERO" />
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
}
